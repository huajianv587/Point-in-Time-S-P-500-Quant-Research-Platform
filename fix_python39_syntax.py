#!/usr/bin/env python3
"""
Fix Python 3.10+ type annotation syntax to be Python 3.9 compatible.
Converts:
- type | None -> Optional[type]
- type1 | type2 -> Union[type1, type2]
- list[...] -> List[...]
- dict[...] -> Dict[...]
- tuple[...] -> Tuple[...]
- set[...] -> Set[...]
"""

import re
import sys
from pathlib import Path
from typing import Set

def fix_file(filepath: Path) -> bool:
    """Fix a single Python file. Returns True if modified."""
    try:
        content = filepath.read_text(encoding='utf-8')
        original = content

        # Check if file already has typing imports
        has_from_import = 'from typing import' in content
        has_import = 'import typing' in content

        # Track which types we need
        needs_optional = False
        needs_union = False
        needs_list = False
        needs_dict = False
        needs_tuple = False
        needs_set = False

        # Fix union types with None (X | None -> Optional[X])
        # This regex matches type | None patterns
        pattern_optional = r'\b([A-Z][A-Za-z0-9_\[\], ]*)\s*\|\s*None\b'
        if re.search(pattern_optional, content):
            needs_optional = True
            content = re.sub(pattern_optional, r'Optional[\1]', content)

        # Fix other union types (X | Y but not with None)
        pattern_union = r'\b([A-Z][A-Za-z0-9_\[\], ]*)\s*\|\s*([A-Z][A-Za-z0-9_\[\], ]*)\b'
        if re.search(pattern_union, content) and '|' in content:
            # Check if there are still unions after Optional replacement
            lines = content.split('\n')
            for i, line in enumerate(lines):
                # Skip comments and strings
                if '#' in line:
                    line = line[:line.index('#')]
                # Find remaining unions
                if ' | ' in line and 'Optional[' not in line:
                    needs_union = True
                    # Replace union syntax (this is a simplified approach)
                    line = re.sub(r'(\w+)\s*\|\s*(\w+)', r'Union[\1, \2]', line)
                    lines[i] = line
            if needs_union:
                content = '\n'.join(lines)

        # Fix lowercase generic types
        if re.search(r'\blist\[', content):
            needs_list = True
            content = re.sub(r'\blist\[', 'List[', content)

        if re.search(r'\bdict\[', content):
            needs_dict = True
            content = re.sub(r'\bdict\[', 'Dict[', content)

        if re.search(r'\btuple\[', content):
            needs_tuple = True
            content = re.sub(r'\btuple\[', 'Tuple[', content)

        if re.search(r'\bset\[', content):
            needs_set = True
            content = re.sub(r'\bset\[', 'Set[', content)

        # If we need to add imports
        if needs_optional or needs_union or needs_list or needs_dict or needs_tuple or needs_set:
            imports_to_add = []
            if needs_optional:
                imports_to_add.append('Optional')
            if needs_union:
                imports_to_add.append('Union')
            if needs_list:
                imports_to_add.append('List')
            if needs_dict:
                imports_to_add.append('Dict')
            if needs_tuple:
                imports_to_add.append('Tuple')
            if needs_set:
                imports_to_add.append('Set')

            # Add imports if needed
            if imports_to_add:
                if has_from_import:
                    # Find existing from typing import line and extend it
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.strip().startswith('from typing import'):
                            # Parse existing imports
                            import_part = line.split('import', 1)[1].strip()
                            existing = [s.strip() for s in import_part.split(',')]
                            # Add new ones
                            for imp in imports_to_add:
                                if imp not in existing:
                                    existing.append(imp)
                            # Rebuild line
                            lines[i] = 'from typing import ' + ', '.join(sorted(existing))
                            break
                    content = '\n'.join(lines)
                else:
                    # Add new import line at the top (after any docstring or __future__)
                    lines = content.split('\n')
                    insert_pos = 0
                    # Skip shebang
                    if lines and lines[0].startswith('#!'):
                        insert_pos = 1
                    # Skip docstrings
                    in_docstring = False
                    for i in range(insert_pos, len(lines)):
                        line = lines[i].strip()
                        if line.startswith('"""') or line.startswith("'''"):
                            if in_docstring:
                                insert_pos = i + 1
                                break
                            in_docstring = True
                        elif line.startswith('from __future__'):
                            insert_pos = i + 1
                        elif line and not line.startswith('#') and not in_docstring:
                            break

                    new_import = 'from typing import ' + ', '.join(sorted(imports_to_add))
                    lines.insert(insert_pos, new_import)
                    content = '\n'.join(lines)

        if content != original:
            filepath.write_text(content, encoding='utf-8')
            return True
        return False

    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return False

def main():
    base_dir = Path(__file__).parent

    # Find all Python files in key directories
    directories = ['gateway', 'agents', 'backtest', 'data', 'quant_rl']

    total = 0
    modified = 0

    for dir_name in directories:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            continue

        for py_file in dir_path.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            total += 1
            if fix_file(py_file):
                modified += 1
                print(f"Fixed: {py_file.relative_to(base_dir)}")

    print(f"\nProcessed {total} files, modified {modified}")

if __name__ == '__main__':
    main()
