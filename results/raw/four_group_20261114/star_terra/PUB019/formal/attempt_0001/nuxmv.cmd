set on_failure_script_quits 1
read_model -i model.smv
go_msat
build_boolean_model
check_invar_ic3
echo === NUXMV_SBMC_PHASE ===
msat_check_ltlspec_sbmc_inc -k 25
echo === NUXMV_LTL_RESULTS ===
check_ltlspec_ic3
quit
