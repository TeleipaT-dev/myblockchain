from rest_framework.views import APIView
from rest_framework.response import Response
from .blockchain import Blockchain
from django.contrib import messages


blockchain = Blockchain()


class MineBlockView(APIView):
    def get(self, request):
        previous_block = blockchain.get_previous_block()
        proof = blockchain.proof_of_work(previous_block["proof"])
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(proof, previous_hash)
        response = {"message": "Новый блок успешно добыт", "block": block}
        return Response(response)


class GetChainView(APIView):
    def get(self, request):
        response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
        return Response(response)


class AddTransactionView(APIView):
    def post(self, request):
        data = request.data
        required_fields = ["sender", "receiver", "amount"]
        if not all(field in data for field in required_fields):
            return Response({"error": "Недостаточно данных"}, status=400)

        index = blockchain.add_transaction(
            sender=data["sender"], receiver=data["receiver"], amount=data["amount"]
        )
        return Response({"message": f"Транзакция добавлена в блок {index}"}, status=201)


from django.shortcuts import render, redirect
from .blockchain import Blockchain

blockchain = Blockchain()


def view_chain(request):
    return render(request, "blockchain_app/chain.html", {"chain": blockchain.chain})


def mine_block(request):
    if request.method == "POST":
        previous_block = blockchain.get_previous_block()
        proof = blockchain.proof_of_work(previous_block["proof"])
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(proof, previous_hash)
        messages.success(request, f"Блок #{block['index']} успешно добыт!")
        return redirect("view_chain")
    return render(request, "blockchain_app/mine.html")


def add_transaction(request):
    if request.method == "POST":
        sender = request.POST.get("sender")
        receiver = request.POST.get("receiver")
        amount = request.POST.get("amount")
        blockchain.add_transaction(sender, receiver, amount)
        messages.success(
            request,
            f"Транзакция от {sender} к {receiver} на {amount} успешно добавлена!",
        )
        return redirect("view_chain")
    return render(request, "blockchain_app/transaction.html")
