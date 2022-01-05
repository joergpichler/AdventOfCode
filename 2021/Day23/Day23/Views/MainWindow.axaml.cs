using Avalonia;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using Day23.ViewModels;

namespace Day23.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
#if DEBUG
            this.AttachDevTools();
#endif
        }

        public MainWindowViewModel ViewModel => (MainWindowViewModel) DataContext;

        private void InitializeComponent()
        {
            AvaloniaXamlLoader.Load(this);
        }

        private void Window_OnKeyDown(object? sender, KeyEventArgs e)
        {
            var key = e.Key;

            if (key == Key.A)
            {
                key = Key.Left;
            }
            else if (key == Key.W)
            {
                key = Key.Up;
            }
            else if (key == Key.S)
            {
                key = Key.Down;
            }
            else if (key == Key.D)
            {
                key = Key.Right;
            }

            if (key is Key.Left or Key.Up or Key.Right or Key.Down)
            {
                ViewModel.Move(key);
            }
        }

        private void Window_OnPointerPressed(object? sender, PointerPressedEventArgs e)
        {
            if (e.MouseButton != MouseButton.Left)
            {
                return;
            }

            if (e.Source is IDataContextProvider {DataContext: GameItem gameItem})
            {
                ViewModel.Click(gameItem);
            }
        }

        private void UndoButton_OnClick(object? sender, RoutedEventArgs e)
        {
            ViewModel.Undo();
        }

        private void ResetButton_OnClick(object? sender, RoutedEventArgs e)
        {
            ViewModel.Reset();
        }
    }
}