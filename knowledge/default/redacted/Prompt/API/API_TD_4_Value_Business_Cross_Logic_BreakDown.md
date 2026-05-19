---
source_path: [REDACTED_SECRET]
source_role: api_prompt
canonical_status: canonical
redaction_status: redacted
---
================= LỆNH THỰC THI - CẤU PHẦN 3: KIỂM THỬ NGHIỆP VỤ, LOGIC CHÉO & DATABASE (MARKMAP FORMAT) =================

Sử dụng toàn bộ kiến thức, tài liệu (RSD & PTTK) và quy tắc định dạng Markmap bạn đã ghi nhớ ở PROMPT 0: NẠP KIẾN THỨC VÀ THIẾT LẬP VAI TRÒ (SETUP CONTEXT). Hãy thực thi việc sinh Test Design cho API chỉ định trong mục III. QUY TẮC ĐỌC HIỂU & PHÂN TÍCH TÀI LIỆU (GLOBAL RULES) -> 4. Giới hạn phạm vi dữ liệu (SCOPE LIMITATION - QUAN TRỌNG)

---

## CẤU HÌNH KIỂM SOÁT CẤU PHẦN (TUỲ BIẾN - ĐỌC TRƯỚC KHI THỰC THI)

> **Hướng dẫn sử dụng:** Chỉ khai báo tham số bạn muốn thay đổi. Bỏ trống = giữ nguyên giá trị mặc định (DEFAULT).

```
EG_CHECK : [DEFAULT]
# Giá trị hợp lệ   : DEFAULT | INJECTION_ONLY | EMOJI_ONLY | OFF
# DEFAULT           : Sinh đúng 2 case theo thứ tự Injection → Emoji (chỉ áp dụng cho field Text tự do)
# INJECTION_ONLY    : Chỉ sinh case SQL/XSS Injection, bỏ qua case Emoji
# EMOJI_ONLY        : Chỉ sinh case Emoji và ký tự Unicode đặc biệt, bỏ qua case Injection
# OFF               : Bỏ qua toàn bộ kiểm thử Error Guessing
```

> **Lưu ý:** [BVA], [ECP], [DT] và [ST] KHÔNG có tham số kiểm soát — BẮT BUỘC sinh đầy đủ mọi trường hợp theo đúng thuật toán, không được bỏ qua.

---

## I. MỤC TIÊU VÀ ĐỘ PHỦ (TẬP TRUNG 100% VÀO BUSINESS LOGIC & LUỒNG)

Giả định rằng: Mọi request ở bước này đều đã PASS kiểm tra Header (Cấu phần 1) và Cấu trúc Schema (Cấu phần 2). Mục tiêu của bạn là bẻ gãy các "Business Rules" (Luật nghiệp vụ) được quy định trong tài liệu Use Case (RSD).
Độ phủ bao gồm 2 lớp:
1. Lớp đơn trường (Single-Field):
- [BVA] Boundary Value Analysis: Phân tích giá trị biên cho các trường Số học, Ngày tháng, Số tiền (Min-1, Max+1).
- [ECP] Equivalence Partitioning: Phân vùng invalid nghiệp vụ (Số âm, sai enum, sai format nghiệp vụ, ID không tồn tại).
- [EG] Error Guessing: Sinh *tối đa 2 case* dị thường (Injection, Emoji) cho field dạng Text tự do.
  Quy tắc áp dụng [EG]:
  + CHỈ áp dụng cho field có kiểu dữ liệu String/Text tự do (VD: reason, description, note...).
  + KHÔNG áp dụng cho field dạng ID, Enum, Number, Date.
  + Sinh đúng 2 case theo thứ tự: (1) Security Input (SQL/XSS Injection), (2) Special Characters (Emoji, ký tự đặc biệt Unicode).
2. Lớp đa trường & Trạng thái (Cross-Field & State):
- [DT] Decision Table: Logic ràng buộc chéo giữa 2 hoặc nhiều trường (VD: Từ ngày < Đến ngày; Giá trị min < max).
  Quy tắc áp dụng [DT] khi có ≥3 trường phụ thuộc nhau:
  + Bước 1: Liệt kê tất cả N trường liên quan, mỗi trường có 2 trạng thái: VALID (V) / INVALID (I).
  + Bước 2: Tổ hợp lý thuyết có 2^N combinations. Loại bỏ các tổ hợp không có nghĩa nghiệp vụ.
  + Bước 3: Chỉ giữ lại các combination có thể xảy ra thực tế và có Expected Result khác nhau.
  + Bước 4: Mỗi combination được giữ lại → sinh 1 test condition [DT].
  Ví dụ tổ hợp 3 trường (min_value, max_value, daily_limit):
  | Combination | min_value | max_value | daily_limit | Giữ lại? | Lý do |
  |---|---|---|---|---|---|
  | C1 | V | V | V | ✓ | Happy Path |
  | C2 | I (min>max) | V | V | ✓ | Vi phạm rule min<max |
  | C3 | V | I (max>limit) | V | ✓ | Vi phạm rule max<=limit |
  | C4 | V | V | I (limit<min) | ✓ | Vi phạm rule limit>=min |
  | C5 | I | I | V | ✗ | Không thêm coverage so với C2+C3 riêng lẻ |
  | C6 | I | V | I | ✗ | Không thêm coverage so với C2+C4 riêng lẻ |
  | C7 | V | I | I | ✗ | Không thêm coverage so với C3+C4 riêng lẻ |
  | C8 | I | I | I | ✗ | Quá nhiều lỗi cùng lúc, không định vị được nguyên nhân |

- [ST] State Transition: Điều kiện tiền quyết của hệ thống/Database trước khi gọi API (VD: User phải Active, Chưa có yêu cầu Pending).

## II. LỆNH CẤM (CONSTRAINTS - NGHIÊM NGẶT)

1. CẤM test các case liên quan đến HEADER (Authorization, Token, Content-Type...).
2. CẤM test lại lỗi Schema (Missing key, Empty value, Sai Data Type, Sai Max Length). Mặc định các lỗi này đã được rào ở Cấu phần 2.
3. CẤM Verify Database cho các case Lỗi nghiệp vụ (HTTP 400, 403, 404). (Vì request lỗi sẽ bị từ chối, không lưu DB). Lưu ý: HTTP 500 KHÔNG được liệt kê là expected error trong Test Design. Nếu API trả về HTTP 500, đây là defect không mong đợi - ghi nhận là bug, không phải test condition.
4. BẮT BUỘC phải Verify Database cho case Happy Path (TD_001) mô tả rõ sự thay đổi trạng thái/dữ liệu.

## III. THUẬT TOÁN TƯ DUY (INTERNAL ALGORITHM)

Chạy ngầm quy trình gồm 3 bước sau trước khi xuất kết quả:
- Bước 0: Đọc CẤU HÌNH KIỂM SOÁT CẤU PHẦN ở trên. Ghi nhớ giá trị `EG_CHECK`.
- Bước 1: Sinh TD_001 Happy Path (Luồng thành công). Viết Expected Result mô tả RÕ RÀNG sự thay đổi của Database (Lưu vào bảng nào, status gì, số dư thay đổi ra sao).
- Bước 2: Vòng lặp Nghiệp vụ Đơn trường (Field-by-Field). Duyệt từng field trong Request Payload:
  + Đối chiếu mục "Business Rules" trong RSD: Có Min/Max -> Sinh [BVA]. Có quy tắc Enum/Format/Tồn tại -> Sinh [ECP].
  + Nếu field là Text tự do -> Áp dụng `EG_CHECK`:
    - `DEFAULT`: Sinh đúng 2 case theo thứ tự Injection → Emoji.
    - `INJECTION_ONLY`: Chỉ sinh case Injection, bỏ qua Emoji.
    - `EMOJI_ONLY`: Chỉ sinh case Emoji, bỏ qua Injection.
    - `OFF`: Bỏ qua, không sinh case [EG] nào.
- Bước 3: Quét Logic Chéo & Trạng thái (Global Scan). BẮT BUỘC thực hiện đầy đủ:
  + Tìm các "Điều kiện tiền quyết" trong RSD -> Sinh case [ST] (Account khóa, sai trạng thái...).
  + Tìm các quy tắc "Nếu... thì...", "phụ thuộc vào":
    ++ Nếu chỉ có 2 trường phụ thuộc -> Sinh case [DT] trực tiếp (Vi phạm logic chéo).
    ++ Nếu có >=3 trường phụ thuộc -> Áp dụng quy trình tổ hợp 4 bước ở Mục I để lọc combination có nghĩa, rồi sinh case [DT] cho từng combination được giữ lại.

## IV. VÍ DỤ MẪU OUTPUT (GOLDEN SAMPLE)

Bắt buộc xuất theo format Markmap như ví dụ (chú ý giữ đúng các ký tự #, ##, ###, -)

```
## Value, Business Logic, Cross Logic
<!-- BƯỚC 1: HAPPY PATH & DATA INTEGRITY -->
### TD_P3_001 - [ST] - Happy Path (Dữ liệu và Trạng thái hợp lệ)
- **Steps**: Request body hợp lệ. Hệ thống kiểm tra tài khoản Active và chưa có yêu cầu Pending.
- **Expected**: 
  - HTTP 200, Code 'SUCCESS'. 
  - DB table 'Threshold_Requests': Lưu 1 record mới với status = 'PENDING'.
<!-- BƯỚC 2: KIỂM THỬ NGHIỆP VỤ ĐƠN TRƯỜNG -->
<!-- Lặp Field: 'amount' (Rule: Min 10,000 - Max 50,000,000) -->
### TD_P3_002 - [BVA] - Field 'amount' nhỏ hơn mức tối thiểu (Min-1)
- **Steps**: Request với 'amount' = 9999.
- **Expected**: HTTP 400, Code 'ERR_AMOUNT_TOO_LOW'.
### TD_P3_003 - [ECP] - Field 'account_id' không tồn tại trong hệ thống
- **Steps**: Request với 'account_id' = "999999" (Fake ID).
- **Expected**: HTTP 404, Code 'ERR_ACCOUNT_NOT_FOUND'.
<!-- Lặp Field: 'reason_text' (Type: String/Text tự do) → Áp dụng EG_CHECK -->
### TD_P3_004 - [EG] - Field 'reason_text' chứa chuỗi SQL Injection
- **Steps**: Request với 'reason_text' = "' OR '1'='1'; DROP TABLE Threshold_Requests; --".
- **Expected**: HTTP 400, Code 'ERR_INVALID_INPUT' HOẶC HTTP 200 nhưng giá trị được lưu DB phải là chuỗi được escape/sanitize an toàn (không được thực thi câu lệnh SQL). TUYỆT ĐỐI không được trả về HTTP 500 (dấu hiệu lỗ hổng SQL Injection thực sự).
### TD_P3_005 - [EG] - Field 'reason_text' chứa ký tự Emoji và Unicode đặc biệt
- **Steps**: Request với 'reason_text' = "Yêu cầu khẩn 🚨🔥 — ký tự đặc biệt: <script>alert(1)</script>".
- **Expected**: HTTP 400, Code 'ERR_INVALID_INPUT' HOẶC HTTP 200 nhưng hệ thống phải xử lý an toàn (encode HTML entities, không render script). Không được trả về HTTP 500.
<!-- BƯỚC 3: KIỂM THỬ TRẠNG THÁI VÀ LOGIC CHÉO -->
### TD_P3_006 - [ST] - Tài khoản đang ở trạng thái bị khóa (INACTIVE)
- **Steps**: Gửi request với 'account_id' thuộc về một tài khoản đã bị khóa.
- **Expected**: HTTP 403, Code 'ERR_ACCOUNT_LOCKED'.
<!-- Ví dụ [DT] với 2 trường phụ thuộc -->
### TD_P3_007 - [DT] - Ngưỡng tối thiểu lớn hơn ngưỡng tối đa (Logic chéo 2 trường)
- **Steps**: Request với 'min_value' = 50000 nhưng 'max_value' = 10000.
- **Expected**: HTTP 400, Code 'ERR_MIN_GREATER_THAN_MAX'.
<!-- Ví dụ [DT] khi có ≥3 trường phụ thuộc (min_value, max_value, daily_limit)
     Sau khi chạy quy trình tổ hợp 4 bước, chỉ giữ lại C2, C3, C4 (xem bảng ở Mục I).
     C1 = Happy Path đã có ở TD_P3_001. Sinh tiếp các combination còn lại: -->
### TD_P3_008 - [DT] - 'max_value' vượt quá hạn mức giao dịch trong ngày 'daily_limit' (C3)
- **Steps**: Request với 'min_value' = 10000, 'max_value' = 200000000, 'daily_limit' = 100000000 (max_value > daily_limit).
- **Expected**: HTTP 400, Code 'ERR_MAX_EXCEEDS_DAILY_LIMIT'.
### TD_P3_009 - [DT] - 'daily_limit' nhỏ hơn 'min_value', vi phạm ràng buộc 3 chiều (C4)
- **Steps**: Request với 'min_value' = 500000, 'max_value' = 10000000, 'daily_limit' = 100000 (daily_limit < min_value).
- **Expected**: HTTP 400, Code 'ERR_DAILY_LIMIT_TOO_LOW'.
<!-- Tiếp tục tăng dần NNN cho đến khi hết các rule... -->
```

## V. THỰC THI CUỐI

1. Tự Self-Audit: Đã xóa hết case test lỗi Schema (thiếu/rỗng trường) chưa? Có verify DB cho case lỗi nào không? (Nếu có -> Xóa ngay). [EG] có áp dụng đúng giá trị `EG_CHECK` không? (DEFAULT = 2 case, INJECTION_ONLY = 1 case, EMOJI_ONLY = 1 case, OFF = không có case nào). [DT] với ≥3 trường có chạy quy trình tổ hợp và loại combination dư thừa chưa? Có bỏ sót case [BVA], [ECP], [DT], [ST] nào không? (Nếu có -> Bổ sung ngay).
2. Rendering: Xuất kết quả dưới dạng MỘT FILE MARKDOWN DUY NHẤT nằm trong code fence. KHÔNG in thêm bất kỳ văn bản/bảng biểu nào khác ngoài luồng.