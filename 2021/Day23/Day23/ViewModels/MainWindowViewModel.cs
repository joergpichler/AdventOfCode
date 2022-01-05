using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Reflection;
using Avalonia.Input;
using ReactiveUI;

namespace Day23.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        private int _score;

        public MainWindowViewModel()
        {
            var lines = Assembly.GetExecutingAssembly().GetEmbeddedResourceLines("Game.txt").ToList();
            for (var iRow = 0; iRow < lines.Count; iRow++)
            {
                var line = lines[iRow];
                for (var iCol = 0; iCol < line.Length; iCol++)
                {
                    var c = line[iCol];
                    if (c == '#')
                    {
                        Items.Add(new Wall(iRow, iCol));
                    }
                    else if (c == 'A' || c == 'B' || c == 'C' || c == 'D')
                    {
                        Items.Add(new Pod(iRow, iCol, c));
                    }
                }
            }

            DetermineHomeAreas(Items.OfType<Pod>().ToArray());
        }

        public int Score
        {
            get => _score;
            private set => this.RaiseAndSetIfChanged(ref _score, value);
        }

        private readonly Dictionary<string, Area> _homeAreas = new()
        {
            {"A", new Area(3)},
            {"B", new Area(5)},
            {"C", new Area(7)},
            {"D", new Area(9)}
        };

        private readonly Stack<Move> _moves = new();

        private Move _currentMove;

        public ObservableCollection<GameItem> Items { get; } = new();

        public void Click(GameItem gameItem)
        {
            var pods = Items.OfType<Pod>().ToList();
            if (pods.Any(p => p.IsLocked))
            {
                return;
            }

            if (gameItem is Pod {IsSelected: true})
            {
                return;
            }

            foreach (var pod in pods)
            {
                pod.IsSelected = false;
            }

            DetermineCanMove();

            if (_currentMove is { IsValid: true })
            {
                _moves.Push(_currentMove);
            }

            _currentMove = null;

            if (gameItem is Pod {CanMove: true} p)
            {
                p.IsSelected = true;

                _currentMove = new Move(p);
            }
        }

        public void Move(Key key)
        {
            var pod = Items.OfType<Pod>().FirstOrDefault(x => x.IsSelected);
            if (pod == null)
            {
                return;
            }

            var newCol = pod.Col;
            if (key == Key.Left)
            {
                newCol -= 1;
            }
            else if (key == Key.Right)
            {
                newCol += 1;
            }

            var newRow = pod.Row;
            if (key == Key.Up)
            {
                newRow -= 1;
            }
            else if (key == Key.Down)
            {
                newRow += 1;
            }

            var itemAtNewLocation = Items.FirstOrDefault(x => x.Row == newRow && x.Col == newCol);
            if (itemAtNewLocation != null)
            {
                return;
            }

            pod.Move(newRow, newCol);

            CheckLocked(pod);
            CalcScore();
            DetermineHomeAreas(pod);
            DetermineCanMove();
        }

        private void CheckLocked(Pod pod)
        {
            // locked is col 3,5,7,9 in row 1
            if (pod.Row == 1 && pod.Col is 3 or 5 or 7 or 9)
            {
                pod.IsLocked = true;
            }
            else
            {
                pod.IsLocked = false;
            }
        }

        private void CalcScore()
        {
            Score = Items.OfType<Pod>().Sum(x => x.Cost);
        }

        private void DetermineHomeAreas(params Pod[] pods)
        {
            foreach (var pod in pods)
            {
                var homeArea = _homeAreas[pod.Type];
                if (pod.Col == homeArea.Col && (pod.Row == homeArea.Rows[0] || pod.Row == homeArea.Rows[1]))
                {
                    pod.IsInTargetArea = true;
                }
                else
                {
                    pod.IsInTargetArea = false;
                }
            }
        }

        private void DetermineCanMove()
        {
            var pods = Items.OfType<Pod>().ToList();
            foreach (var pod in pods.Where(x => x.Row == 1 && !x.IsSelected))
            {
                var canMove = true;

                var homeArea = _homeAreas[pod.Type];
                var pod1 = pods.FirstOrDefault(p => p.Col == homeArea.Col && p.Row == homeArea.Rows[0]);
                var pod2 = pods.FirstOrDefault(p => p.Col == homeArea.Col && p.Row == homeArea.Rows[1]);
                if (pod1 != null && pod1.Type != pod.Type)
                {
                    canMove = false;
                }

                if (pod2 != null && pod2.Type != pod.Type)
                {
                    canMove = false;
                }

                pod.CanMove = canMove;
            }
        }

        public void Undo()
        {
            var selected = Items.OfType<Pod>().FirstOrDefault(p => p.IsSelected);
            if (selected != null)
            {
                selected.IsSelected = false;
                if (_currentMove is { IsValid: true })
                {
                    _moves.Push(_currentMove);
                }

                _currentMove = null;
            }

            if (_moves.Count == 0)
            {
                return;
            }

            var move = _moves.Pop();

            move.Undo();
            move.Pod.CanMove = true;
            CalcScore();
            DetermineCanMove();
            DetermineHomeAreas(move.Pod);
        }

        public void Reset()
        {
            var selected = Items.OfType<Pod>().FirstOrDefault(p => p.IsSelected);
            if (selected != null)
            {
                selected.IsSelected = false;
                if (_currentMove is { IsValid: true })
                {
                    _moves.Push(_currentMove);
                }

                _currentMove = null;
            }

            while (_moves.Count > 0)
            {
                Undo();
            }
        }
    }
}