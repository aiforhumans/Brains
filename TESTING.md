# Testing Guidelines for Brains-XDEV

## Quick Verification

### 1. Node Import Test
Start ComfyUI and verify you see this message in the terminal:
```
[Brains-XDEV] hello node import
```

### 2. Node Availability Test
In ComfyUI's interface:
1. Right-click to open the node search
2. Search for "Brains-XDEV"
3. Verify "Brains-XDEV • Hello (echo)" appears under `Brains-XDEV/Test`

### 3. Node Functionality Test
1. Add the Hello node to a workflow
2. Connect it to appropriate inputs/outputs
3. Test that it echoes the input text with "Echo: " prefix

## Development Testing

### Running Tests
```powershell
# From the project root
C:\comfy\ComfyUI_windows_portable\python_embeded\python.exe -m pytest tests/
```

### Installing Test Dependencies
```powershell
C:\comfy\ComfyUI_windows_portable\python_embeded\python.exe -m pip install pytest
```

## Troubleshooting

### Node Not Appearing
1. Check ComfyUI terminal for Python import errors
2. Verify symlink is correctly pointing to `src/` directory
3. Restart ComfyUI after code changes
4. Clear `__pycache__` folders if needed

### Import Errors
1. Check that all required dependencies are installed in ComfyUI's embedded Python
2. Verify file paths and imports in your node code
3. Check ComfyUI's console output for detailed error messages

### Symlink Issues
1. Ensure you're running PowerShell as Administrator
2. Try using junction (`mklink /J`) instead of symlink (`mklink /D`)
3. Verify the target paths exist and are correct

## Best Practices

1. **Always test after code changes** - ComfyUI may need restart for major changes
2. **Use the embedded Python** - Don't mix system Python with ComfyUI's embedded interpreter
3. **Check imports early** - Fix import errors before testing node functionality
4. **Clean builds** - Remove `__pycache__` folders when debugging import issues