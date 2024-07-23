import random
from collections.abc import Generator

import algopy
import pytest
from algopy.op import itob
from algopy_testing import AlgopyTestContext, algopy_testing_context

from smart_contracts.ama_proof.contract import AmaProof


# khoi tao moi truong va ngu canh
@pytest.fixture()
def context() -> Generator[AlgopyTestContext, None, None]:
    with algopy_testing_context() as ctx:
        yield ctx
        ctx.reset()


def test_init(context: AlgopyTestContext) -> None:
    contract = AmaProof()
    contract.__init__()

    assert contract.max_viewer == algopy.UInt64(30)
    assert contract.total_viewer == algopy.UInt64(0)
    assert contract.asset_url == algopy.String("ipfs://...0xla")


def test_confirm_joined(context: AlgopyTestContext) -> None:
    contract = AmaProof()
    contract.__init__()

    contract.confirm_joined()
    # address = context.any_account;

    # fuzzing testing
    assert context.get_box(context.default_creator.bytes) == itob(1)
    assert contract.total_viewer == algopy.UInt64(1)

    try:
        contract.confirm_joined()
        raise Exception("account allow joined twice")
    except AssertionError:
        assert True

    account = context.any_account()
    context.patch_txn_fields(sender=account)
    contract.confirm_joined()

    assert contract.total_viewer == algopy.UInt64(2)
    assert context.get_box(account.bytes) == itob(2)

    contract.total_viewer = 30
    account = context.any_account()
    context.patch_txn_fields(sender=account)
    try:
        contract.confirm_joined()
        raise Exception("over maximum")
    except AssertionError:
        assert True


def test_get_pov_id(context: AlgopyTestContext) -> None:
    contract = AmaProof()
    contract.__init__()
    num = random.randint(0, 100)
    account = context.any_account()
    context.patch_txn_fields(sender=account)
    context.set_box(account.bytes, itob(num))

    pov_id = contract.get_pov_id()

    assert pov_id == algopy.UInt64(num), "get pov id failed"


def test_claim_pov_token(context: AlgopyTestContext) -> None:
    contract = AmaProof()
    contract.__init__()

    pov_id = random.randint(0, 100)
    account = context.any_account()
    context.set_box(account.bytes, itob(pov_id))

    winner_id = random.randint(0, 100)
    winner = context.any_account()
    context.set_box(winner.bytes, itob(winner_id))

    # not winner
    try:
        contract.claim_pov_token()
        raise Exception("Not winner")
    except AssertionError:
        assert True

    contract.winner = winner

    context.patch_txn_fields(sender=account)

    try:
        contract.claim_pov_token()
        raise Exception("Not winner")
    except AssertionError:
        assert True

    context.patch_txn_fields(sender=winner)

    contract.claim_pov_token()

    assert contract.reward_claimed == algopy.UInt64(winner_id), "claim pov token failed"


def test_send_pov_token(context: AlgopyTestContext) -> None:
    contract = AmaProof()
    contract.__init__()

    try:
        contract.send_pov_token()
        raise Exception("Not winner")
    except AssertionError:
        assert True

    winner_id = random.randint(0, 100)
    winner = context.any_account()
    context.set_box(winner.bytes, itob(winner_id))

    contract.winner = winner
    context.patch_txn_fields(sender=winner)
    contract.claim_pov_token()

    context.patch_txn_fields(sender=context.default_creator)
    contract.send_pov_token()
