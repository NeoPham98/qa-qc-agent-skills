# UI Test Design

**Project**: PAYGATES  
**Epic**: UI-UAT sample  
**Source**: BIDV UI/RSD/PTTK sample evidence  

### TD_001 - [ECP] - Đăng nhập thành công với thông tin hợp lệ
- **Steps**: Mở màn hình đăng nhập PAYGATES, nhập username/password hợp lệ, chọn Đăng nhập.
- **Expected**: Dashboard hiển thị, tên người dùng và menu chức năng đúng vai trò.
- **Source**: RSD login flow section.

### TD_002 - [ECP] - Đăng nhập thất bại khi mật khẩu sai
- **Steps**: Mở màn hình đăng nhập PAYGATES, nhập username hợp lệ và password sai, chọn Đăng nhập.
- **Expected**: Người dùng vẫn ở màn hình đăng nhập và thông báo lỗi xác thực hiển thị.
- **Source**: RSD login validation section.
