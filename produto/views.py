from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Categoria, Produto, Adicional, Opcoes


# Create your views here.
def home(req):
    if not req.session.get("carrinho"):
        req.session["carrinho"] = []
        req.session.save()
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    return render(
        req,
        "home.html",
        context={
            "produtos": produtos,
            "categorias": categorias,
            "carrinho": len(req.session["carrinho"]),
        },
    )


def categorias(request, id):
    produtos = Produto.objects.filter(categoria_id=id)
    categorias = Categoria.objects.all()

    return render(
        request,
        "home.html",
        {
            "produtos": produtos,
            "carrinho": len(request.session["carrinho"]),
            "categorias": categorias,
        },
    )


def produto(req, id):
    if not req.session.get("carrinho"):
        req.session["carrinho"] = []
        req.session.save()
    produto = Produto.objects.get(id=id)
    erro = req.GET.get("erro")
    categorias = Categoria.objects.all()
    return render(
        req,
        "produto.html",
        context={
            "produto": produto,
            "categorias": categorias,
            "carrinho": len(req.session["carrinho"]),
            "erro": erro,
        },
    )


def add_carrinho(req):
    if not req.session.get("carrinho"):
        req.session["carrinho"] = []
        req.session.save()

    x = {**req.POST}

    def removeLixo():
        adicionais = x.copy()
        adicionais.pop("id")
        adicionais.pop("csrfmiddlewaretoken")
        adicionais.pop("observacoes")
        adicionais.pop("quantidade")
        adicionais = list(cada for cada in adicionais.items())
        return adicionais

    adicionais = removeLixo()

    # a = {"ok": [1, 2, 3], "notok": "notok", "maybe": 1}
    # b = tuple(cada for cada in a.items())
    # print("...", b)

    # return HttpResponse(adicionais)
    id = int(x["id"][0])
    print("<<<", x)
    prod = Produto.objects.filter(id=id)[0]
    preco_total = prod.preco
    adicionais_verifica = Adicional.objects.filter(produto=id)
    print(">>>", adicionais_verifica)
    aprovado = True
    for i in adicionais_verifica:
        encontrou = False
        minimo = i.minimo
        maximo = i.maximo
        for j in adicionais:
            if i.nome == j[0]:
                encontrou = True
                if len(j[1]) < minimo or len(j[1]) > maximo:
                    aprovado = False
        if minimo > 0 and encontrou == False:
            aprovado = False
    if not aprovado:
        return redirect(f"/produto/{id}?erro=1")

    for i, j in adicionais:
        for k in j:
            preco_total += Opcoes.objects.filter(id=int(k))[0].acrescimo

    def troca_id_por_nome_adicional(adicional):
        adicionais_com_nome = []
        for i in adicionais:
            opcoes = []
            for j in i[1]:
                op = Opcoes.objects.filter(id=int(j))[0].nome
                opcoes.append(op)
            adicionais_com_nome.append((i[0], opcoes))
        return adicionais_com_nome

    adicionais = troca_id_por_nome_adicional(adicionais)

    preco_total *= int(x["quantidade"][0])
    data = {
        "id_produto": int(x["id"][0]),
        "observacoes": x["observacoes"][0],
        "preco": preco_total,
        "adicionais": adicionais,
        "quantidade": x["quantidade"][0],
    }

    req.session["carrinho"].append(data)
    req.session.save()
    # return HttpResponse(req.session["carrinho"])
    return redirect(f"/produto/ver_carrinho")


def ver_carrinho(req):
    categorias = Categoria.objects.all()
    dados_mostrar = []
    for cada in req.session["carrinho"]:
        print(">>>", cada)
        prod = Produto.objects.filter(id=cada["id_produto"])
        dados_mostrar.append(
            {
                "imagem": prod[0].img.url,
                "nome": prod[0].nome_produto,
                "quantidade": cada["quantidade"],
                "preco": cada["preco"],
                "id": cada["id_produto"],
            }
        )
    total = sum([float(cada["preco"]) for cada in req.session["carrinho"]])
    return render(
        req,
        "carrinho.html",
        context={
            "dados": dados_mostrar,
            "total": total,
            "carrinho": len(req.session["carrinho"]),
            "categorias": categorias,
        },
    )


def remover_carrinho(request, id):
    request.session["carrinho"].pop(id)
    request.session.save()
    return redirect("/produto/ver_carrinho/")
