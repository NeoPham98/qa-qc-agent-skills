# Kế Hoạch Kiểm Thử

**Mã Kế Hoạch Kiểm Thử**: TP-CCTG-ONLINE-001
**Dự án**: CCTG_Online
**Nhóm**: Squad_Customer
**Epic**: Customer_Validate
**Môi trường**: SIT
**Phiên bản phát hành**: 2026.05.20-rc1

## Phạm vi áp dụng

- Kiểm thử tính đúng đắn của API kiểm tra điều kiện khách hàng (`POST /v1/customer/validate`) thuộc phạm vi CCTG Online.
- Bao gồm thiết kế kịch bản test (Test Design), xuất kịch bản thủ công ra file Excel định dạng chuẩn.

## Phạm vi loại trừ

- Phê duyệt triển khai Production và kiểm định tích hợp hệ thống bên ngoài không thuộc phạm vi kế hoạch này.

## Tài liệu căn cứ

| Mã tài liệu | Loại tài liệu | Phạm vi |
|---|---|---|
| source-manifest#source-1 | runtime_input | Tài liệu đặc tả API check điều kiện KH mua CCTG OL PDF |

## Yêu cầu căn cứ

| Mã yêu cầu | Tài liệu căn cứ | Trạng thái | Ghi chú |
|---|---|---|---|
| REQ-CCTG-001 | source-manifest#source-1 | Có | Kiểm tra các điều kiện: quốc tịch (101), tuổi (102), loại khách hàng (103), tình trạng cư trú (104), giờ giao dịch COT (109) |

## Mức độ / Giai đoạn kiểm thử

| Giai đoạn | Mục đích | Người thực hiện | Môi trường | Điều kiện bắt đầu | Sản phẩm đầu ra |
|---|---|---|---|---|---|
| SIT | Kiểm tra mã lỗi trả về và độ ưu tiên lỗi | Trưởng nhóm QA | SIT | Tài liệu căn cứ được duyệt | Test Design và Test Case được ký duyệt |
| UAT | Xác nhận nghiệp vụ và tính đúng đắn tích hợp | BA Owner | UAT | SIT hoàn thành | Tài liệu bàn giao UAT |

## Điều kiện bắt đầu

- Tài liệu baselines nguồn đã được chuẩn hóa và sẵn sàng.
- Môi trường SIT đã sẵn sàng kết nối dữ liệu giả lập khách hàng.

## Điều kiện kết thúc

- 100% các kịch bản kiểm thử đã được chạy thành công.
- Không còn lỗi nghiêm trọng (Blocker/Major) chưa được giải quyết.
- Báo cáo Test Plan, Test Design và Test Cases được ký duyệt đầy đủ.

## Sản phẩm bàn giao

| Sản phẩm | Bắt buộc | Người chịu trách nhiệm | File đầu ra |
|---|---|---|---|
| Kế hoạch kiểm thử | Có | Trưởng nhóm QA | TestPlan.md và TestPlan.generated.xlsx |
| Thiết kế kịch bản | Có | Trưởng nhóm QA | API_TestDesign.md và API_TestDesign.generated.xlsx |
| Danh sách kịch bản | Có | Tester | TestCaseSource.md và Legacy19TestCase.generated.xlsx |

## Vai trò và Trách nhiệm

| Vai trò | Trách nhiệm | Người thực hiện |
|---|---|---|
| Trưởng nhóm QA | Lập kế hoạch, duyệt sản phẩm và điều phối | QA Lead |
| Tester | Thiết kế kịch bản, chạy test và báo cáo lỗi | Tester |

## Môi trường / Dữ liệu / Phụ thuộc

| Hạng mục | Giá trị | Người quản lý | Trạng thái |
|---|---|---|---|
| Môi trường SIT | SIT-cctg-online | Env Team | Sẵn sàng |
| Dữ liệu test | Danh sách CIF thỏa mãn các mã lỗi | Data Team | Sẵn sàng |

## Rủi ro và Giải pháp

| Rủi ro | Mức độ ảnh hưởng | Giải pháp giảm thiểu | Người chịu trách nhiệm |
|---|---|---|---|
| Môi trường SIT gián đoạn | Chậm tiến độ | Sử dụng mock API kiểm tra lỗi tại local | QA Lead |

## Lịch trình / Mốc thời gian

| Mốc thời gian | Ngày dự kiến | Người thực hiện | Kết quả đầu ra |
|---|---|---|---|
| Phê duyệt Test Plan | 2026-05-20 | QA Lead | Ký duyệt TestPlan.md/xlsx |
| Thiết kế kịch bản test | 2026-05-21 | Tester | Ký duyệt Test Design & Test Cases |

## Chiến lược độ bao phủ

Tính liên kết giữa yêu cầu và kịch bản test sẽ được duy trì. Mỗi mã lỗi nghiệp vụ (101, 102, 103, 104, 109) phải được bao phủ tối thiểu bởi một Test Design node tương ứng.

## Câu hỏi cần làm rõ

| Mã câu hỏi | Tài liệu căn cứ | Nội dung câu hỏi | Người trả lời | Hạn trả lời |
|---|---|---|---|---|
| OQ-001 | source-manifest#source-1 | Có áp dụng kiểm tra giờ giao dịch COT đối với người nước ngoài không? | BA Owner | 2026-05-21 |
