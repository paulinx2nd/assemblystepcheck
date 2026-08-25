"""Five-validator GLSim flow for screened, verified, hash-chained assembly."""

import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


GRAPH = {"steps": [{"id": "BASE", "instruction": "Align and fasten the two base rails, then record a level and fastener check.", "requires": []}, {"id": "FRAME", "instruction": "Attach the upright frame to the verified base and record the alignment and torque checks.", "requires": ["BASE"]}]}


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context():
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {"Screen public assembly evidence": json.dumps({"result": "READY_FOR_VERIFIER"})}},
    )
    return {"validators": [validator.to_dict() for validator in validators]}


def test_five_validator_prerequisite_and_verifier_flow():
    designer_account, builder_account, verifier_account = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "assembly_step_check.py")
    deployed = factory.deploy_contract_tx(args=[], account=designer_account, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(deployed)
    address = extract_contract_address(deployed)
    designer = factory.build_contract(address, account=designer_account)
    builder = factory.build_contract(address, account=builder_account)
    verifier = factory.build_contract(address, account=verifier_account)
    plan_id = f"{str(designer_account.address).lower()}:BENCH"
    build_id = f"{str(builder_account.address).lower()}:BUILD-1"
    _ok(designer.publish_plan(args=["BENCH", "Community bench assembly", GRAPH]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(builder.start_build(args=[plan_id, "BUILD-1", verifier_account.address, "One flat-pack community bench identified by public kit reference BENCH-2026-A."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    steps = [("BASE", "Both base rails were aligned on the marked surface, all specified fasteners were installed, and a level check showed no visible deviation.", "Base evidence and physical alignment checks are accepted by the verifier."), ("FRAME", "The upright frame was attached to the verified base, the specified fasteners were torqued, and alignment was checked at both sides.", "Frame evidence and physical alignment checks are accepted by the verifier.")]
    for step_id, evidence, note in steps:
        _ok(builder.submit_step(args=[build_id, step_id, evidence]).transact(transaction_context=_context(), wait_transaction_status=TransactionStatus.FINALIZED))
        _ok(verifier.verify_step(args=[build_id, step_id, True, note]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(builder.close_build(args=[build_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    build = builder.get_build(args=[build_id]).call()
    assert build["status"] == "COMPLETE"
    assert build["chain_head"].startswith("sha256:")
