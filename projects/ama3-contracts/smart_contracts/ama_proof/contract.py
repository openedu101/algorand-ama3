import algopy
from algopy import Account, ARC4Contract, Asset, String, Txn, UInt64, subroutine
from algopy.arc4 import abimethod


class AmaProof(ARC4Contract):
    # Function -> ProofOfViewer (time, 50) -> whitelist (address, nft)
    # Mint NFT -> Wallet -> address -> nft (asset.id)
    # Oracle Front-end -> Claim POV(ProofOfViewer) Token NFT

    def __init__(self) -> None:
        self.max_viewer = UInt64(30)
        self.asset_url = String("ipfs://...0xla")
        self.total_viewer = UInt64(0)
        self.winner = Account()
        self.reward_claimed = UInt64(0)

    # Todo -> Who is winner
    # ko dung vao
    def choose_winner(self, addr: Account) -> None:
        pass

    # -->>> Region:: START  --->>>  Confirm
    @abimethod()
    def confirm_joined(self) -> None:
        # Assert Require
        assert self.total_viewer < self.max_viewer, "Maximum"
        # Luu tru thong tin nguoi tham gia
        # mapping(address -> asset.id)
        # address -> value
        _id, already_exists = algopy.op.Box.get(Txn.sender.bytes)  # address -> bytes
        # true -> not true -> false -> error
        assert not already_exists, "Already claim POV"
        # Execute
        minted_asset = self._mint_pov(Txn.sender)
        # self.total_viewer = self.total_viewer + 1
        self.total_viewer += 1

        # input address -> Box
        algopy.op.Box.put(Txn.sender.bytes, algopy.op.itob(minted_asset.id))

    # <<<-- Region:: END    <<<---  Confirm

    # -->>> Internal:: START  --->>>  Function Mint NFT
    @subroutine
    def _mint_pov(self, claimer: Account) -> Asset:
        # ASA -> Algorand Standard Assets
        algopy.ensure_budget(UInt64(10000), algopy.OpUpFeeSource.AppAccount)
        asset_name = b"Openedu Algorand #" + claimer.bytes
        # submit -> tao NFT
        return (
            algopy.itxn.AssetConfig(
                asset_name=asset_name,
                unit_name=String("EDU"),
                url=self.asset_url,
                manager=claimer,
                total=UInt64(1),
                decimals=0,
            )
            .submit()
            .created_asset  # asset.id
        )

    # <<<-- Internal:: END    <<<---  Function Mint NFT

    @abimethod
    def get_pov_id(self) -> UInt64:
        # get -> op.Box.get(sender) -> asset.id
        pov_id, exists = algopy.op.Box.get(Txn.sender.bytes)
        assert exists, "POV not found"
        return algopy.op.btoi(pov_id)

    @abimethod
    def claim_pov_token(self) -> None:
        # tao NFT -> AssetConfig -> asset - Reward.
        # winner == Txn.sender -> NFT
        # require
        assert Txn.sender == self.winner, "Only winner can claim"
        assert self.reward_claimed == 0, "Reward already claimed"
        self.reward_claimed = self.get_pov_id()

    @abimethod
    def send_pov_token(self) -> None:
        # itxn.AssetTransfer(
        # asset_id, from, to, amount
        # )
        assert self.reward_claimed != 0, "Reward not claimed yet"
        algopy.itxn.AssetTransfer(
            xfer_asset=self.reward_claimed, asset_receiver=self.winner, asset_amount=1
        ).submit()
