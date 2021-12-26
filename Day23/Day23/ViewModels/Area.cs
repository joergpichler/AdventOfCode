namespace Day23.ViewModels
{
    public class Area
    {
        public Area(int col)
        {
            Col = col;
            Rows = new []{2,3};
        }

        public int Col { get; }

        public int[] Rows { get; }
    }
}