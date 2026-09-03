using System;

namespace PCControlApp.Models
{
    /// <summary>
    /// CẤU TRÚC KẾT QUẢ KIỂM TRA MỘT SẢN PHẨM (CHIP APPLE A18)
    /// Đóng vai trò là DTO (Data Transfer Object) truyền dữ liệu giữa:
    /// Thuật toán Xử lý ảnh (Vision Engine) -> Bộ não điều phối (ViewModel) -> Màn hình (View)
    /// </summary>
    public class InspectionResult
    {
        public int ProductId { get; set; }
        public string SerialNumber { get; set; } = "UNKNOWN";
        public double Width { get; set; }
        public double Height { get; set; }
        public double Angle { get; set; }
        public bool IsOk { get; set; }
        public string DefectReason { get; set; } = "PASSED";
        public double CycleTimeMs { get; set; }
        public DateTime Timestamp { get; set; } = DateTime.Now;

        // Thuộc tính tiện ích hiển thị lên giao diện
        public string VerdictText => IsOk ? "PASS (OK)" : $"FAIL (NG - {DefectReason})";
        public string StatusColor => IsOk ? "#22C55E" : "#EF4444"; // Xanh lá hoặc Đỏ
        public string FormattedTime => Timestamp.ToString("HH:mm:ss.fff");
    }
}
