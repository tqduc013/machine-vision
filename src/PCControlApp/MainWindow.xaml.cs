using System.Windows;
using Wpf.Ui.Controls;

namespace PCControlApp
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// Kế thừa Wpf.Ui.Controls.FluentWindow chuẩn Windows 11 Fluent Design
    /// </summary>
    public partial class MainWindow : FluentWindow
    {
        public MainWindow()
        {
            InitializeComponent();
        }
    }
}