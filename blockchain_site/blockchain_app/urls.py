from django.urls import path
from .views import MineBlockView, GetChainView, AddTransactionView

urlpatterns = [
    path("mine_block/", MineBlockView.as_view()),
    path("get_chain/", GetChainView.as_view()),
    path("add_transaction/", AddTransactionView.as_view()),
]
from django.urls import path
from .views import view_chain, mine_block, add_transaction

urlpatterns = [
    path("", view_chain, name="view_chain"),
    path("mine/", mine_block, name="mine_block"),
    path("add/", add_transaction, name="add_transaction"),
]
