import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from pedido.models import CupomDesconto, ItemPedido, Pedido

from produto.models import Categoria, Produto


# Create your views here.
def finalizar_pedido(req):
    if req.method == "GET":
        categorias = Categoria.objects.all()
        erro = req.GET.get("erro")
        total = sum(float(i["preco"]) for i in req.session["carrinho"])
        
        return render(
            req,
            "finalizar_pedido.html",
            context={
                "carrinho": len(req.session["carrinho"]),
                "categorias": categorias,
                "erro": erro,
                "total": total,
            },
        )
    else:
        if len(req.session["carrinho"]) == 0:
            return redirect("/pedidos/finalizar_pedido?erro=1")
        dados = req.POST
        total = sum(float(i["preco"]) for i in req.session["carrinho"])
        cupom = CupomDesconto.objects.filter(codigo=dados["cupom"])
        cupom_salvar = None
        if len(cupom) > 0 and cupom[0].ativo:
            total = total - ((total * cupom[0].desconto) / 100)
            cupom[0].usos += 1
            cupom[0].save()
            cupom_salvar = cupom[0]
        carrinho = req.session.get("carrinho")
        listaCarrinho = []
        for item in carrinho:
            listaCarrinho.append(
                {
                    "produto": Produto.objects.filter(id=item["id_produto"])[0],
                    "observacoes": item["observacoes"],
                    "preco": item["preco"],
                    "adicionais": item["adicionais"],
                    "quantidade": item["quantidade"],
                }
            )

        lambda_func_troco = (
            lambda x: int(x["troco_para"]) - total if not x["troco_para"] == "" else ""
        )
        lambda_func_pagamento = (
            lambda x: "Cartão" if x["meio_pagamento"] == "2" else "Dinheiro"
        )

        pedido = Pedido(
            usuario=dados["nome"],
            total=total,
            troco=lambda_func_troco(dados),
            cupom=cupom_salvar,
            pagamento=lambda_func_pagamento(dados),
            ponto_referencia=dados["pt_referencia"],
            cep=dados["cep"],
            rua=dados["rua"],
            numero=dados["numero"],
            bairro=dados["bairro"],
            telefone=dados["telefone"],
        )
        pedido.save()
        ItemPedido.objects.bulk_create(
            ItemPedido(
                pedido=pedido,
                produto=cada["produto"],
                quantidade=cada["quantidade"],
                preco=cada["preco"],
                adicionais=cada["adicionais"],
            )
            for cada in listaCarrinho
        )
        req.session["carrinho"].clear()
        req.session.save()
        return render(req, "pedido_realizado.html")


def validar_cupom(request):
    cupom = request.POST.get('cupom')
    cupom = CupomDesconto.objects.filter(codigo = cupom)
    if len(cupom) > 0 and cupom[0].ativo:
        desconto = cupom[0].desconto
        total = sum([float(i['preco']) for i in request.session['carrinho']])
        total_com_desconto = total - ((total*desconto)/100)
        data_json = json.dumps({'status': 0,
                                'desconto': desconto,
                                'total_com_desconto': str(total_com_desconto).replace('.', ',')

                                })
        return HttpResponse(data_json)
    else:
        return HttpResponse(json.dumps({'status': 1}))