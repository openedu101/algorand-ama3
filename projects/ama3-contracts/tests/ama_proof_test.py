from collections.abc import Generator

import algopy
from algopy.op import itob
import pytest
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
