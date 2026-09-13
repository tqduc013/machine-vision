namespace PCControlApp.Models
{
    /// <summary>
    /// CẤU TRÚC KẾT QUẢ KIỂM TRA MỘT SẢN PHẨM CÔNG NGHIỆP
    /// Hỗ trợ cả MVTec Metal Nut (Đai ốc công nghiệp) và Bán dẫn (Apple A18 Chip)
    /// Đóng vai trò là DTO (Data Transfer Object) truyền dữ liệu:
    /// Vision Engine -> ViewModel -> View (WPF UI)
    /// </summary>
    public class InspectionResult
    {
        public int ProductId { get; set; }
        public string PartType { get; set; } = "MVTec Metal Nut";
        public string SerialNumber { get; set; } = "UNKNOWN";
        public double Width { get; set; }
        public double Height { get; set; }
        public double Angle { get; set; }
        
        // Thông số đo đạc đai ốc MVTec
        public double InnerDiameter { get; set; }
        public double OuterDiameter { get; set; }
        public string DefectType { get; set; } = "None";
        public double DefectArea { get; set; }

        public bool IsOk { get; set; }
        public string DefectReason { get; set; } = "PASSED";
        public double AnomalyScore { get; set; }
        public string Mode { get; set; } = "Rule-based CV";
        public double CycleTimeMs { get; set; }
        public DateTime Timestamp { get; set; } = DateTime.Now;

        // Thuộc tính tiện ích hiển thị lên giao diện
        public string VerdictText => IsOk ? "PASS (OK)" : $"FAIL (NG - {DefectReason})";
        public string StatusColor => IsOk ? "#22C55E" : "#EF4444"; // Xanh lá hoặc Đỏ
        public string FormattedTime => Timestamp.ToString("HH:mm:ss.fff");
    }
}
