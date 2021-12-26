using ReactiveUI;

namespace Day23.ViewModels
{
    public class GameItem : ReactiveObject
    {
        private const int TileSize = 20;

        private int _row;
        private int _col;

        public GameItem(int row, int col)
        {
            _row = row;
            _col = col;
        }

        public int Row
        {
            get => _row;
            protected set
            {
                if (_row == value)
                {
                    return;
                }
                _row = value;
                this.RaisePropertyChanged();
                this.RaisePropertyChanged(nameof(Top));
            }
        }

        public int Col
        {
            get => _col;
            protected set
            {
                if (_col == value)
                {
                    return;
                }
                _col = value;
                this.RaisePropertyChanged();
                this.RaisePropertyChanged(nameof(Left));
            }
        }

        public int Top => _row * TileSize;

        public int Left => _col * TileSize;
    }
}