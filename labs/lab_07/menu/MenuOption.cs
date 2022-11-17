using System;
using System.Collections.Generic;
using System.Data;

namespace menu_system
{
    public abstract class MenuOption
    {
        public readonly char? Key;
        public readonly string Name;

        public ConsoleColor? ForegroundColor { get; set; }
        public ConsoleColor? BackgroundColor { get; set; }

        public abstract void Activate();

        public virtual void NextOption() { }

        public virtual void PreviousOption() { }

        public virtual string CurrentOption()
        {
            return Name;
        }

        protected MenuOption(string name, char? key, ConsoleColor? foregroundColor, ConsoleColor? backgroundColor)
        {
            Name = name;
            ForegroundColor = foregroundColor;
            BackgroundColor = backgroundColor;
            Key = key;
        }

        protected MenuOption(ConsoleColor? foregroundColor, ConsoleColor? backgroundColor, char? key)
        {
            ForegroundColor = foregroundColor;
            BackgroundColor = backgroundColor;
            Key = key;
            throw new NotImplementedException();
        }
    }

    public class MenuOptionWithAction : MenuOption
    {
        private readonly Action _action;

        public MenuOptionWithAction(
            string name,
            Action action,
            char? key = null,
            ConsoleColor? foregroundColor = null,
            ConsoleColor? backgroundColor = null) : base(name, key,
            foregroundColor,
            backgroundColor)
        {
            _action = action;
        }

        public override void Activate()
        {
            _action.Invoke();
        }
    }

    public class MenuOptionWithSubMenu : MenuOption
    {
        private readonly Menu _submenu;

        public MenuOptionWithSubMenu(
            string name,
            Menu submenu,
            char? key = null,
            ConsoleColor? foregroundColor = null,
            ConsoleColor? backgroundColor = null) : base(name, key,
            foregroundColor,
            backgroundColor)
        {
            _submenu = submenu;
        }

        public override void Activate()
        {
            _submenu.Run();
        }
    }

    public class MenuOptionWithStringSelector : MenuOption
    {
        private readonly List<string> _options;
        private readonly Action<string> _onChange;
        private int _selection;

        public int Selection
        {
            get => _selection;
            set
            {
                if (value >= 0 && value < _options.Count)
                {
                    _selection = value;
                }
                else
                {
                    throw new Exception("Selection out of index");
                }
            }
        }

        public MenuOptionWithStringSelector(
            string name,
            List<string> options,
            Action<string> onChange,
            char? key = null,
            ConsoleColor? foregroundColor = null,
            ConsoleColor? backgroundColor = null) : base(name, key,
            foregroundColor,
            backgroundColor)
        {
            if (options.Count < 2) throw new Exception("Must have at least 2 options");

            _onChange = onChange;
            _options = options;
            _selection = 0;
        }

        public override void NextOption()
        {
            if (++_selection >= _options.Count) _selection = 0;
            _onChange.Invoke(CurrentOption());
        }

        public override void PreviousOption()
        {
            if (--_selection < 0) _selection = _options.Count - 1;
            _onChange.Invoke(CurrentOption());
        }

        public override string CurrentOption()
        {
            return _options[_selection];
        }

        public override void Activate()
        {
            _onChange.Invoke(CurrentOption());
        }
    }

    public class MenuOptionWithNumberSelector : MenuOption
    {
        private readonly Action<int, int> _onChange;
        private readonly int _start;
        private readonly int _count;
        private readonly int _step;
        private int _selection;

        public int Selection
        {
            get => _selection;
            set
            {
                if (value >= 0 && value < _count)
                {
                    _selection = value;
                }
                else
                {
                    throw new Exception($"Selection out of range: {value}");
                }
            }
        }

        public MenuOptionWithNumberSelector(string name,
            int start,
            int count,
            Action<int, int> onChange,
            int step = 2,
            char? key = null,
            ConsoleColor? foregroundColor = null,
            ConsoleColor? backgroundColor = null) : base(name, key,
            foregroundColor,
            backgroundColor)
        {
            if (count <= 1 || step <= 1)
            {
                throw new Exception("Must have at least 2 sorted options, and positive count and step");
            }

            _onChange = onChange;
            _step = step;
            _start = start;
            _count = count;
            _selection = 0;
        }

        public override void NextOption()
        {
            if (++_selection > _count) _selection = 0;

            _onChange(_selection, (_selection * _step) + _start);
        }

        public override void PreviousOption()
        {
            if (--_selection < 0) _selection = _count;

            _onChange(_selection, (_selection * _step) + _start);
        }

        public override string CurrentOption()
        {
            return ((_selection * _step) + _start).ToString();
        }

        public override void Activate()
        {
            _onChange(_selection, (_selection * _step) + _start);
        }
    }
}