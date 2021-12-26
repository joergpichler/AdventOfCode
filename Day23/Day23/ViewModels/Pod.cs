using ReactiveUI;

namespace Day23.ViewModels
{
    public class Pod : GameItem
    {
        private bool _isSelected;
        private bool _isLocked;
        private bool _isInTargetArea;
        private bool _canMove = true;

        public Pod(int row, int col, char type) : base(row, col)
        {
            Type = type.ToString();
        }

        public string Type { get; }

        public bool IsLocked
        {
            get => _isLocked;
            set => this.RaiseAndSetIfChanged(ref _isLocked, value);
        }

        public int Cost { get; set; }

        public bool IsSelected
        {
            get => _isSelected;
            set => this.RaiseAndSetIfChanged(ref _isSelected, value);
        }

        public bool IsInTargetArea
        {
            get => _isInTargetArea;
            set => this.RaiseAndSetIfChanged(ref _isInTargetArea, value);
        }

        public bool CanMove
        {
            get => _canMove;
            set => this.RaiseAndSetIfChanged(ref _canMove, value);
        }

        public void Move(int newRow, int newCol)
        {
            Row = newRow;
            Col = newCol;

            IncreaseCost();
        }

        private void IncreaseCost()
        {
            var increase = 0;
            switch (Type)
            {
                case "A":
                    increase = 1;
                    break;
                case "B":
                    increase = 10;
                    break;
                case "C":
                    increase = 100;
                    break;
                case "D":
                    increase = 1000;
                    break;
            }

            Cost += increase;
        }
    }
}