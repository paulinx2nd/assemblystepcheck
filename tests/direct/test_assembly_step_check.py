"""Direct tests for prerequisite steps, verifier separation, and hash chaining."""

import json


GRAPH = {
    "steps": [
        {"id": "BASE", "instruction": "Align and fasten the two base rails, then record a level and fastener check.", "requires": []},
        {"id": "FRAME", "instruction": "Attach the upright frame to the verified base and record the alignment and torque checks.", "requires": ["BASE"]},
    ]
}
BASE_EVIDENCE = "Both base rails were aligned on the marked surface, all specified fasteners were installed, and a level check showed no visible deviation."
FRAME_EVIDENCE = "The upright frame was attached to the verified base, the specified fasteners were torqued, and alignment was checked at both sides."


def _plan(contract, direct_vm, designer):
    direct_vm.sender = designer
    return contract.publish_plan("BENCH", "Community bench assembly", GRAPH)


def _build(contract, direct_vm, builder, verifier, plan_id):
    direct_vm.sender = builder
    return contract.start_build(plan_id, "BUILD-1", verifier, "One flat-pack community bench identified by public kit reference BENCH-2026-A.")


def _submit(contract, direct_vm, builder, build_id, step_id, evidence, result="READY_FOR_VERIFIER"):
    direct_vm.sender = builder
    direct_vm.clear_mocks()
    direct_vm.mock_llm(r".*Screen public assembly evidence.*", json.dumps({"result": result}))
    contract.submit_step(build_id, step_id, evidence)


def test_plan_requires_topological_order(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    bad = {"steps": [GRAPH["steps"][1], GRAPH["steps"][0]]}
    with direct_vm.expect_revert("plan_must_be_topologically_ordered"):
        contract.publish_plan("BAD", "Broken plan ordering", bad)


def test_verifier_must_be_distinct(contract, direct_vm, direct_alice, direct_bob):
    plan_id = _plan(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("verifier_must_be_distinct"):
        contract.start_build(plan_id, "BAD", direct_bob, "A build cannot verify its own evidence under this workflow.")


def test_locked_step_cannot_be_submitted(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    plan_id = _plan(contract, direct_vm, direct_alice)
    build_id = _build(contract, direct_vm, direct_bob, direct_charlie, plan_id)
    with direct_vm.expect_revert("prerequisites_not_verified"):
        contract.submit_step(build_id, "FRAME", FRAME_EVIDENCE)


def test_screen_and_verifier_acceptance_unlock_next_step(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    plan_id = _plan(contract, direct_vm, direct_alice)
    build_id = _build(contract, direct_vm, direct_bob, direct_charlie, plan_id)
    genesis = contract.get_build(build_id)["chain_head"]
    _submit(contract, direct_vm, direct_bob, build_id, "BASE", BASE_EVIDENCE)
    direct_vm.sender = direct_charlie
    contract.verify_step(build_id, "BASE", True, "Base evidence and physical alignment checks are accepted by the verifier.")
    build = contract.get_build(build_id)
    assert build["steps"][1]["status"] == "AVAILABLE"
    assert build["chain_head"] != genesis


def test_verifier_rejection_returns_step_to_rework(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    plan_id = _plan(contract, direct_vm, direct_alice)
    build_id = _build(contract, direct_vm, direct_bob, direct_charlie, plan_id)
    _submit(contract, direct_vm, direct_bob, build_id, "BASE", BASE_EVIDENCE)
    direct_vm.sender = direct_charlie
    contract.verify_step(build_id, "BASE", False, "The verifier found the level check incomplete and requests a new measurement.")
    step = contract.get_build(build_id)["steps"][0]
    assert step["status"] == "REWORK"
    assert step["rework_count"] == 1


def test_all_verified_steps_close_build(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    plan_id = _plan(contract, direct_vm, direct_alice)
    build_id = _build(contract, direct_vm, direct_bob, direct_charlie, plan_id)
    _submit(contract, direct_vm, direct_bob, build_id, "BASE", BASE_EVIDENCE)
    direct_vm.sender = direct_charlie
    contract.verify_step(build_id, "BASE", True, "Base step accepted after independent alignment and fastener checks.")
    _submit(contract, direct_vm, direct_bob, build_id, "FRAME", FRAME_EVIDENCE)
    direct_vm.sender = direct_charlie
    contract.verify_step(build_id, "FRAME", True, "Frame step accepted after independent alignment and torque checks.")
    direct_vm.sender = direct_bob
    contract.close_build(build_id)
    assert contract.get_build(build_id)["status"] == "COMPLETE"


def test_invalid_screening_output_preserves_available_step(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    plan_id = _plan(contract, direct_vm, direct_alice)
    build_id = _build(contract, direct_vm, direct_bob, direct_charlie, plan_id)
    direct_vm.mock_llm(r".*Screen public assembly evidence.*", json.dumps({"result": "DONE"}))
    with direct_vm.expect_revert("invalid_screen_result"):
        contract.submit_step(build_id, "BASE", BASE_EVIDENCE)
    assert contract.get_build(build_id)["steps"][0]["status"] == "AVAILABLE"
