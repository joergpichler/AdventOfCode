namespace Day23.ViewModels
{
    public class Move
    {
        public Pod Pod { get; }

        public Move(Pod pod)
        {
            Pod = pod;
            Cost = pod.Cost;
            Col = pod.Col;
            Row = pod.Row;
        }

        public int Row { get; }

        public int Col { get; }

        public int Cost { get; }

        public bool IsValid => Row != Pod.Row || Col != Pod.Col;

        public void Undo()
        {
            Pod.Move(Row, Col);
            Pod.Cost = Cost;
        }
    }
}