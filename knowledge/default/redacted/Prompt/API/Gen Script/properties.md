---
source_path: Prompt/API/Gen Script/properties.txt
source_role: sensitive_config
canonical_status: sensitive_reference
redaction_status: redacted
---
testLinkIntegration=Serenityf
testLinkUser=hiepnd1
testLinkKey=[REDACTED_SECRET]
testLinkBuildName= SIT_Auto_Deposit_4_0_0
testLinkPlanName=Auto_Deposit_4_0_0

#URL & Endpoint

Token_Base=https:[REDACTED_SECRET]
[REDACTED_SECRET]
[REDACTED_SECRET]; [REDACTED_SECRET]; [REDACTED_SECRET]; [REDACTED_SECRET]
Token_Authorization=Bearer [REDACTED_SECRET]

InvestmentSweepAdd1_BaseURL=https:[REDACTED_SECRET]
AD_4_0_0_BaseURL=http:[REDACTED_SECRET]
AD_Trans_Create = /v1/trans/transCreate
AD_Trans_Request = /v1/trans/transRequest
AD_Trans_Approve = /v1/trans/approveProcess
AD_Trans_Cancel = /v1/trans/transCancel
AD_Min_Val = /v1/trans/minval
AD_Min_Val_Submit = /v1/trans/minval/submit
AD_Approve=/v1/trans/minval/approve
AD_Reject=/v1/trans/minval/reject
AD_Trans_Search = /v1/trans/search

#Data

ID_GDV_CN_1=157733
ID_GDV_HO_1=180519
ID_KSV_HO_1=171919
PASSWORD=[REDACTED_CREDENTIAL]
BRN_GDV_CN_1 = 120000
BRN_GDV_HO_1 = 990000

cif=1175
acctNo = 8854741208
transStaff = 150100

#Database
nmsbl_hostname=[REDACTED_INTERNAL_ENDPOINT]
nmsbl_port=1521
nmsbl_serviceName=nmsbl
nmsbl_username=QLTGTT_SIT
nmsbl_password=QLTGTT_SIT123123

