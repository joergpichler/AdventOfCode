using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using Avalonia;
using Avalonia.Data.Converters;
using Avalonia.Media;

namespace Day23.Views
{
    public class PodToBackgroundConverter : IMultiValueConverter
    {
        public object Convert(IList<object> values, Type targetType, object parameter, CultureInfo culture)
        {
            if (values.Any(v => v is UnsetValueType))
            {
                return Brushes.Transparent;
            }

            var isInTargetArea = (bool) values[0];
            var canMove = (bool) values[1];

            if (isInTargetArea)
            {
                return Brushes.Green;
            }

            if (!canMove)
            {
                return Brushes.Red;
            }

            return Brushes.Transparent;
        }
    }
}