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
    assert contract.asset_id == algopy.UInt64(0)
    assert contract.winner == algopy.Account()


def test_confirm_joined(context: AlgopyTestContext) -> None:
    contract = AmaProof()
    contract.__init__()

    contract.confirm_joined()
    # address = context.any_account;

    # fuzzing testing
    assert context.get_box(context.default_creator.bytes) == itob(1)
    assert contract.total_viewer == algopy.UInt64(1)


def test_mint_pov(context: AlgopyTestContext) -> None:
    contract = AmaProof()
    contract.__init__()

    contract._mint_pov(context.default_creator)

def test_get_pov_id(context: AlgopyTestContext) -> None:
    contract = AmaProof()
    contract.__init__()

    assert contract.get_pov_id() == algopy.UInt64(1)


def test_claim_pov_token(context: AlgopyTestContext) -> None:
    contract = AmaProof()
    contract.__init__()

    contract.claim_pov_token()
    assert contract.asset_id == algopy.UInt64(0)
    assert contract.winner == algopy.Account(context.default_creator.bytes)


def test_send_pov_token(context: AlgopyTestContext) -> None:
    contract = AmaProof()
    contract.__init__()

    contract.send_pov_token()
    assert contract.asset_id == algopy.UInt64(1)
