using MathNet.Numerics.LinearAlgebra;

static class Matrices
{
    private static readonly List<Matrix<double>> _transformationMatrices = new();

    public static IReadOnlyCollection<Matrix<double>> TransformationMatrices => _transformationMatrices;

    public static Matrix<double> IdentityMatrix { get; }

    static Matrices()
    {
        for (var sX = 0; sX < 2; sX++)
        {
            for (var sY = 0; sY < 2; sY++)
            {
                for (var sZ = 0; sZ < 2; sZ++)
                {
                    for (var iX = 0; iX < 3; iX++)
                    {
                        for (var iY = 0; iY < 3; iY++)
                        {
                            for (var iZ = 0; iZ < 3; iZ++)
                            {
                                if (iX == iY)
                                {
                                    continue;
                                }

                                if (iX == iZ)
                                {
                                    continue;
                                }

                                if (iY == iZ)
                                {
                                    continue;
                                }

                                var m = Matrix<double>.Build.Dense(3, 3);
                                m[iX, 0] = sX == 0 ? 1 : -1;
                                m[iY, 1] = sY == 0 ? 1 : -1;
                                m[iZ, 2] = sZ == 0 ? 1 : -1;

                                var det = (int) m.Determinant();

                                if (m.Column(0).Count(x => x != 0) != 1 ||
                                    m.Column(1).Count(x => x != 0) != 1 ||
                                    m.Column(2).Count(x => x != 0) != 1)
                                {
                                    throw new Exception();
                                }

                                if (det == 1)
                                {
                                    _transformationMatrices.Add(m);
                                }

                                if ((int)m[0, 0] == 1 && (int) m[1, 1] == 1 && (int) m[2, 2] == 1)
                                {
                                    IdentityMatrix = m;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}