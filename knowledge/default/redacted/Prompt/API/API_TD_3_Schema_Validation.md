---
source_path: [REDACTED_SECRET]
source_role: api_prompt
canonical_status: reference
redaction_status: redacted
---
================= LỆNH THỰC THI - CẤU PHẦN 2: SCHEMA VALIDATION (MARKMAP FORMAT) =================

Sử dụng toàn bộ kiến thức, tài liệu (RSD & PTTK) và quy tắc định dạng Markmap bạn đã ghi nhớ ở PROMPT 0: NẠP KIẾN THỨC VÀ THIẾT LẬP VAI TRÒ (SETUP CONTEXT). Hãy thực thi việc sinh Test Design cho API chỉ định trong mục III. QUY TẮC ĐỌC HIỂU & PHÂN TÍCH TÀI LIỆU (GLOBAL RULES) -> 4. Giới hạn phạm vi dữ liệu (SCOPE LIMITATION - QUAN TRỌNG)

I. MỤC TIÊU VÀ ĐỘ PHỦ (CHỈ TẬP TRUNG SCHEMA)
Chỉ kiểm thử Cấu trúc dữ liệu (Schema) của Request Body/Params dựa trên bảng PTTK:
- [Missing] / [Empty] Mandatory Check: Check sự tồn tại theo cột "Required/Bắt buộc". CHỈ TẠO 2 case: Missing key và Empty value. (TUYỆT ĐỐI KHÔNG TẠO CASE TRUYỀN NULL).
- [Type] Data Type Check: Check sai kiểu dữ liệu (VD: String thay vì Integer, Object thay vì Array) theo cột "Kiểu dữ liệu".
- [Max Length] Length Constraint: Check vi phạm độ dài chuỗi ký tự theo cột "Max Length" (VD: Nhập N+1 ký tự). CHỈ CHECK nếu CÓ con số cụ thể.

II. LỆNH CẤM (CONSTRAINTS - NGHIÊM NGẶT)
1. KHÔNG sinh test case liên quan đến HEADER (Authorization, Token...). 
2. KHÔNG TẠO case truyền null khi check Mandatory. Chỉ dùng Missing và Empty.
3. KHÔNG TỰ BỊA / ASSUME con số Max Length nếu tài liệu không ghi. (Không ghi = Bỏ qua check length).
4. KHÔNG test logic nghiệp vụ (Số âm, min/max value, business rules) hay logic chéo ở prompt này.
5. KHÔNG Verify DB cho các case Validation lỗi (HTTP 400). Chỉ Verify DB cho case Happy Path (TD_001).

III. THUẬT TOÁN TƯ DUY (INTERNAL ALGORITHM)
Chạy ngầm quy trình sau trước khi xuất kết quả:
- Bước 1: Sinh TD_001 Happy Path (Valid Schema) - Request chứa đầy đủ các trường đúng định dạng.
- Bước 2: Vòng lặp Field-by-Field. Duyệt tuần tự từng field trong Request Payload (Bỏ qua Header). 
Với mỗi field (F), thực hiện ĐÚNG THỨ TỰ:
  + Check Required (Y) -> Sinh Missing & Empty.
  + Check Type -> Sinh sai định dạng cơ bản.
  + Check Max Length (Nếu có) -> Sinh N+1 ký tự.
  + Check Min Length (Nếu có) -> Sinh case nhỏ hơn số ký tự cho phép
BẮT BUỘC xong field F mới chuyển sang field tiếp theo.

IV. VÍ DỤ MẪU OUTPUT (GOLDEN SAMPLE)
Bắt buộc xuất theo format Markmap như ví dụ (chú ý giữ đúng các ký tự #, ##, ###, -):
## Schema Validation
### TD_P2_001 - [ST] - Happy Path Full Flow (Valid Schema)
- **Steps**: Request body với đầy đủ thông tin hợp lệ.
- **Expected**: HTTP 200, Code 'SUCCESS'. DB lưu 1 record mới.
<!-- BẮT ĐẦU VÒNG LẶP FIELD: 'amount' (Type: Integer, Required: Y, Max-len: Không có) -->
### TD_P2_002 - [Missing] - Field 'amount' bị Missing
- **Steps**: Request body thiếu key 'amount' (Check Required).
- **Expected**: HTTP 400, Code 'ERR_MISSING_FIELD'.
### TD_P2_003 - [Empty] - Field 'amount' truyền rỗng
- **Steps**: Request với 'amount' = "" (Check Empty).
- **Expected**: HTTP 400, Code 'ERR_MISSING_FIELD'.
### TD_P2_004 - [Type] - Field 'amount' sai kiểu dữ liệu (String)
- **Steps**: Request với 'amount' = "một triệu" (Check Type).
- **Expected**: HTTP 400, Code 'ERR_INVALID_TYPE'.
<!-- Lặp tiếp cho các field khác, ID NNN tiếp tục tăng dần... -->

V. THỰC THI CUỐI
1. Tự Self-Audit: Đã xóa hết case test Header chưa? Có case Null nào không? Có tự bịa Max Length không?
2. Rendering: Xuất kết quả dưới dạng MỘT FILE MARKDOWN DUY NHẤT nằm trong code fence. KHÔNG in thêm bất kỳ văn bản/bảng biểu nào khác ngoài luồng.