using System;
using System.IO;
using System.Windows;
using System.Windows.Threading;

namespace PCControlApp;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        AppDomain.CurrentDomain.UnhandledException += (s, args) =>
        {
            File.WriteAllText("app_crash.log", args.ExceptionObject.ToString());
        };

        DispatcherUnhandledException += (s, args) =>
        {
            File.WriteAllText("app_crash.log", args.Exception.ToString());
            args.Handled = true;
        };
    }
}

