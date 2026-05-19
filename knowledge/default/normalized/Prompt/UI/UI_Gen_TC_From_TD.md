---
source_path: Prompt/UI/UI_Gen_TC_From_TD.txt
source_role: ui_prompt
canonical_status: canonical
redaction_status: unredacted
---
================= PROMPT GEN MANUAL TEST CASE WEB UI FROM TEST DESIGN MARKDOWN =================

I. MỤC TIÊU CHÍNH
Sinh FULL bộ **Manual Test Cases chi tiết (19 cột)** cho TẤT CẢ các màn hình Web UI, dựa trên **Test Design dạng Markdown (Markmap)** và file RSD đã sinh ở bước trước.

1. Test Design Input = File Markdown cấu trúc cây (#, ##,###,  -).
2. Nhiệm vụ của prompt này:
   - Convert từng Node Test Condition (###) trong Markdown thành **nhiều Test Case chi tiết đảm bảo mức test coverage chi tiết cao nhất**.
   - Mỗi Test Case có:
     + Pre-conditions cụ thể (được suy luận mở rộng thêm từ Steps high-level và file RSD).
     + Test Datas đủ giá trị cụ thể.
     + Test Steps chi tiết, đánh số 1., 2., 3., …
     + Expected result chi tiết, mapping với từng bước verify.
3. Đảm bảo mỗi màn hình / flow vẫn có đủ 5 kỹ thuật:
   1) ECP
   2) BVA
   3) Decision Table
   4) State Transition
   5) Error Guessing

Output DUY NHẤT:
- 1 file TSV trong code fence (```tsv ... ```), encoding UTF-8 with BOM, đúng CONTRACT 19 cột.
- KHÔNG in phân tích, KHÔNG in Test Design, KHÔNG in giải thích ngoài code fence TSV.

II. NGUỒN DỮ LIỆU & VAI TRÒ

1. Test Design Markdown (Đầu vào chính)
   - Đây là file được sinh từ prompt “PROMPT GEN TEST DESIGN WEB UI FROM RSD DẠNG MARKMAP”.
   - Cấu trúc file:
     + `## Function Name` -> Tên màn hình/chức năng.
     + `### [ID][Technique] Test Condition Summary` -> Định nghĩa Test Condition.
     + `- **Steps**: ...` -> Các bước thực hiện high-level.
     + `- **Expected**: ...` -> Kết quả mong đợi high-level.
   - **Test Design là “source of truth” về coverage**: KHÔNG tự thêm/bớt Test Condition ngoài danh sách các Node `###` đã có.

2. RSD Web UI & PTTK-UI (Dữ liệu bổ trợ)
   - Dùng để:
     + Chi tiết hóa các step high-level thành step click/type cụ thể.
     + Lấy tên field, rules (maxlength, format) để sinh Test Datas cụ thể.
     + Lấy mã lỗi, câu thông báo chính xác để điền vào Expected Result.

3. PTTK-UI
   - Dùng để:
     + Biết API nào được gọi ở mỗi thao tác.
     + Mapping field UI ↔ request/response API.
     + Behavior UI sau khi API trả SUCCESS/FAIL.
     + Hành vi đặc biệt: double-click, pagination, icon action, popup confirm…

4. Danh sách mã lỗi (nếu có)
   - Mã lỗi, thông điệp, loại lỗi (VALIDATION/BUSINESS/SYSTEM…).

Nguyên tắc:
- COVERAGE phải **bám theo Test Design**, không tự nghĩ thêm Test Condition mới.
- Chỉ được sử dụng RSD/PTTK để:
  + Chi tiết hóa Test Datas, Test Steps, Expected result.
  + Không được sinh thêm kỹ thuật/Scenario Outline ngoài những gì đã có trong Test Design.

III. QUAN HỆ GIỮA TEST DESIGN MARKDOWN VÀ TEST CASE

1. **1 Node `###` trong Markdown** (1 Test Condition) có thể sinh ra:
   - **1 Test Case**: Nếu logic đơn giản, chỉ cần 1 bộ data đại diện.
   - **N Test Case**: Nếu condition đó cần nhiều giá trị data để cover (VD: Boundary cần test min-1 và max+1, hoặc ECP cần test nhiều loại ký tự đặc biệt khác nhau).

2. Logic Mapping:
   - Markdown Header `### [001][ST] Truy cập thành công`
     -> `Test Case ID` gốc = 001
     -> `Group Tests` = State Transition (ST)
     -> `Test Case Summary` = Truy cập thành công...

IV. ĐỊNH DẠNG OUTPUT TSV (CONTRACT 19 CỘT – MANUAL TEST CASE)

1. Header (CHÍNH XÁC, thứ tự không đổi, quote all):
"Test Case ID" "Function" "Group Tests" "Scenario Outline" "Test Case Summary" "Pre-conditions" "Test Datas" "Test Steps" "Expected result" "Environment" "Priority" "Regression" "Automation" "Manual Test Results Round 1" "Manual Test Results Round 2" "Automation Test Results" "Actual result" "BugID" "Notes"

2. Mỗi Test Case 1 dòng (SINGLE_LINE_MODE). Trong ô có thể xuống dòng logic bằng ký tự \n (KHÔNG xuống dòng thật).
3. Delimiter: Tab (\t). Mỗi dòng có đúng **18 tab** (19 cột).
4. Quote ALL cells. Escape " bên trong bằng "".
5. Encoding: UTF-8 with BOM.
6. Không dòng trống cuối, không ký tự thừa sau Test Case cuối.
7. Cột Notes luôn là "" (rỗng).
8. Assumption chỉ được đặt trong Test Case Summary (vd “[ASSUMPTION: …]”).

V. QUY ĐỊNH CHI TIẾT CHO 19 CỘT

1. "Test Case ID"
   - Format: `<MarkdownID>_TC_<NNN>`
   - Trong đó:
     + `<MarkdownID>`: Là ID lấy trong cặp ngoặc vuông đầu tiên của header `###`. Ví dụ `TD_[005]` -> `TD_005`.
     + `<NNN>`: tăng dần từ 001 cho đến testcase cuối cùng, không testcase nào trùng NNN.
   - Ví dụ: Node `## [TD_001][ECP]...` sinh ra 2 test cases:
     -> `TD_001_TC_001`
     -> `TD_001_TC_002`
	Node `## [TD_002][ECP]...` sinh ra 3 test cases:
     -> `TD_002_TC_003`
     -> `TD_002_TC_004`
     -> `TD_002_TC_005`

2. "Function"
   - Lấy từ Header `##` gần nhất bên trên node đó.
   - Ví dụ: `## 1. Khởi tạo & Phân quyền` -> Function = "Khởi tạo & Phân quyền".

3. "Group Tests"
   - Parse từ tag thứ 2 trong header `###`.
   - Mapping:
     + `[ECP]` -> ECP
     + `[BVA]` -> BVA
     + `[DT]` -> Decision Table
     + `[ST]` -> State Transition
     + `[EG]` -> Error Guessing

4. "Scenario Outline"
   - Vì Markdown không có cột này, hãy trích xuất **Cụm từ chính** trong `Test Condition Summary` của node `###`.
   - Ví dụ: `### [TD_012][BVA] Ngày tiếp nhận - Khoảng thời gian hợp lệ`
     -> Scenario Outline = "Ngày tiếp nhận - Khoảng thời gian hợp lệ"

5. "Test Case Summary"
   - Phát triển từ `Test Condition Summary` từ Markdown + **Giá trị cụ thể** của Test Case này.
     + Giữ ý nghĩa partition/boundary/state.
     + Bổ sung thêm **giá trị cụ thể** đang test.
   - Ví dụ:
     - Markdown: `[ECP] Username hợp lệ (tài khoản tồn tại, trạng thái ACTIVE)`
       → Test Case Summary:
         + `Kiểm tra login với Username hợp lệ = "user01" (trạng thái ACTIVE) và Password hợp lệ`
   - Nếu có ASSUMPTION từ Test Design:
     + Sao chép + giữ nguyên prefix [ASSUMPTION: …] ở cuối Summary.

6. "Pre-conditions"
   - Phân tích từ `- **Steps**:` high-level trong Markdown và chức năng tương ứng trong file RSD.
Ví dụ:
   - Nếu Step ghi: "User đăng nhập nhưng không có quyền..." -> Pre-condition: "User đã đăng nhập, Role = 'User thường', Permission = OFF".
   - Nếu Step ghi: "Data setup: 1 bản ghi có vi phạm..." -> Pre-condition: "Trong DB có sẵn 1 bản ghi thỏa mãn điều kiện vi phạm...".

7. "Test Data"
   - Cực kỳ quan trọng: Phải convert mô tả high-level thành Key="Value" cụ thể nếu có thể hoặc mô tả kiểu dữ liệu của data.
   - Ví dụ Markdown: "Nhập chuỗi ký tự đặc biệt"
     -> Output TSV: `SearchKey="Select * from Users #"`
   - Không được ghi: "Data hợp lệ", "Data sai".

   - Nguyên tắc:
     + KHÔNG được viết mơ hồ: "Data hợp lệ", "Data không hợp lệ", "max length OK".
     + Mỗi Test Case phải ghi rõ giá trị cụ thể đang test (đặc biệt cho maxlength, boundary, domain).
   - Nếu Test Design nói `Boundary length: 0,1,20,21`:
     + Có thể tạo nhiều Test Case, mỗi case 1 giá trị cụ thể:
       * Case 1: Username="" (length=0)
       * Case 2: Username="A" (length=1)
       * Case 3: Username="ABCDEFGHIJKLMNOPQRST" (length=20)
       * Case 4: Username="ABCDEFGHIJKLMNOPQRSTU" (length=21)

8. "Test Steps"
   - Phát triển thêm dòng `- **Steps**:` trong Markdown và file RSD thành các bước thao tác chi tiết 1., 2., 3.
- Trong ô có thể xuống dòng logic bằng ký tự \n (KHÔNG xuống dòng thật).
   - Skeleton chuẩn:
     1) Mở màn hình (hoặc truy cập URL).
     2) Nhập/Chọn từng field với giá trị từ Test Datas.
     3) Thực hiện hành động (click button/link/icon…).
     4) Nếu nhiều màn hình: nêu rõ đang ở màn hình nào khi thao tác.
     5) Bước verify (1 hoặc nhiều bước) sau thao tác.
   - Ví dụ:
     1. Mở trình duyệt và truy cập URL trang Đăng nhập <Login_URL>
     2. Nhập Username = "user01" vào ô "Tên đăng nhập"
     3. Nhập Password = "P@ss123" vào ô "Mật khẩu"
     4. Click button "Đăng nhập"
     5. Kiểm tra hệ thống chuyển tới màn hình "Trang chủ" theo RSD
   - YÊU CẦU:
     + Mỗi step bắt đầu bằng "1. ", "2. ", "3. "… (KHÔNG dùng "- B1", "Step 1"…).
     + Ghi rõ đang ở màn hình nào khi thao tác (đặc biệt với flow nhiều màn hình).

9. "Expected result"
  - Phát triển thêm dòng `- **Expected**:` trong Markdown và file RSD thành chi tiết.
  - Phát triển từ Expected high-level + thông tin RSD/PTTK:
  - Mỗi assertion một dòng (dùng \n trong cell), bắt buộc phải đánh số trùng với số bước VERIFY ở cột Test Steps.
      (Bước thao tác không cần Expected. Chỉ bước verify mới sinh Expected tương ứng.) ví dụ:
	+ Hệ thống hiển thị màn hình "Trang chủ" theo RSD mục [Màn hình Trang chủ]
	+ Không hiển thị thông báo lỗi
	+ Trên góc phải hiển thị tên người dùng = "Nguyễn Văn A"
	+ Bảng kết quả tìm kiếm hiển thị 10 dòng, có ít nhất 1 dòng có Mã KH = "CUST001"
    + Mapping với các bước verify trong Test Steps. Bước thao tác không cần Expected. Chỉ bước verify mới sinh Expected tương ứng.
  - Expected result phải mô tả RÕ:
	+ Màn hình nào được hiển thị sau thao tác.
	+ Thông điệp hiển thị (nếu có): nội dung, vị trí tương đối (popup / dòng dưới field / banner trên cùng… nếu RSD có).
	+ Trạng thái field / button (disable/enable/readonly… nếu RSD mô tả).
	+ Dữ liệu hiển thị trong bảng / danh sách (VD: số dòng, giá trị cột chính, trạng thái…).
  - Với các thao tác có gọi API (theo PTTK-UI): phải mô tả rõ Expected liên quan đến API, bao gồm:
	+ API nào được gọi (tên API, hoặc endpoint nếu PTTK có).
	+ Trạng thái trả về: SUCCESS / FAIL / lỗi hệ thống (theo RSD/PTTK).
	+ Mã lỗi, thông điệp từ API (nếu dùng để hiển thị UI).
	+ Behavior UI tương ứng với response API (enable/disable nút, highlight dòng, hiển thị popup…).
  - Với các thao tác dẫn đến ghi dữ liệu (insert/update vào Database): phải mô tả Expected về trạng thái DB, bao gồm:
	+ Bản ghi được tạo mới/thay đổi đúng theo giá trị input.
	+ Trạng thái, số lượng bản ghi, giá trị cột quan trọng phải đúng.
	+ Không tạo bản ghi thừa, không ghi duplicate (nếu RSD/PTTK quy định).
	+ Chỉ verify DB nếu trong RSD/PTTK có mô tả rõ hành vi ghi dữ liệu.
   - KHÔNG verify UI/UX về màu sắc/layout/responsive nếu RSD/PTTK không mô tả.
- Trong ô có thể xuống dòng logic bằng ký tự \n (KHÔNG xuống dòng thật).
10. "Environment"
    - Ghi rõ môi trường dự kiến chạy:
      + "DEV", "SIT", "UAT", "PREPROD"… hoặc "ALL".
    - Có thể tham chiếu từ Pre-conditions.

11. "Priority"
    - Đánh mức độ ưu tiên thực thi:
      + "High" cho path nghiệp vụ chính, rule quan trọng.
      + "Medium" cho case phổ biến.
      + "Low" cho Error Guessing, edge case ít quan trọng (nếu phù hợp).

12. "Regression"
    - "Yes" nếu Test Case nên nằm trong bộ Regression.
    - "No" nếu chỉ chạy theo đợt.
    - Nếu chưa rõ, có thể để "".

13. "Automation"
    - "Yes" nếu Test Case nên được automation (không phụ thuộc nhiều vào thao tác khó tự động).
    - "No" nếu khó automation (ví dụ, captcha, email ngoài…).

14–19. "Manual Test Results Round 1" … "BugID" "Notes"
    - Để "" (rỗng) trong output ban đầu.

VI. KỸ THUẬT KIỂM THỬ & COVERAGE (TÁI ÁP DỤNG TỪ TEST DESIGN)

1. ECP:
   - Đảm bảo mỗi partition/class trong Test Design được thể hiện bằng ≥1 Test Case có data cụ thể.

2. BVA:
   - Mỗi boundary point được thể hiện ít nhất 1 Test Case có giá trị cụ thể.

3. Decision Table:
   - Mỗi rule/row trong Decision Table (all-valid, single-invalid, multi-mix) phải có Test Case tương ứng.

4. State Transition:
   - Mỗi state chuyển quan trọng (FORM_EMPTY → FORM_INVALID → FORM_VALID → SUBMIT_SUCCESS/SUBMIT_FAIL) phải có Test Case.

5. Error Guessing:
   - Các tình huống nhạy cảm phải có Test Case với Test Datas cụ thể (chuỗi dài, ký tự đặc biệt, back/refresh…).

VI. HƯỚNG DẪN XỬ LÝ ASSUMPTION
- Nếu trong Markdown có `[ASSUMPTION]`:
  -> Đưa nội dung đó vào cuối "Test Case Summary".
  -> Tự định nghĩa Expected Result hợp lý nhất dựa trên logic Web App thông thường (nếu RSD thiếu).

VII. THỰC THI CUỐI (CHO AI)

1. Đọc toàn bộ nội dung file **Test Design dạng Markdown (Markmap)**.
2. Với từng Test Condition:
   - Parse ID, Technique, Title.
   - Đọc Steps/Expected high-level.
   - Đọc Test Case Summary, Pre-conditions, Test Datas, Expected result.
   - Dựa vào RSD + PTTK-UI để cụ thể hóa thành nhiều Manual Test Case đảm bảo mức test coverage chi tiết cao nhất.
3. Sinh FULL bộ Test Case 19 cột theo quy tắc trên (ECP/BVA/DT/ST/EG đầy đủ).
4. Self-audit theo checklist mục VII.
5. Xuất DUY NHẤT 1 code fence ```tsv ... ``` chứa toàn bộ Manual Test Case 19 cột.
6. KHÔNG in thêm bất kỳ giải thích, bảng, chữ nào ngoài code fence TSV.

================= KẾT THÚC PROMPT =================