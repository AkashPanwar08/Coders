/* Disable copy option */
globalVariable.editorCodeBlock.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_C, () => null);

/*Disable select option */
globalVariable.editorCodeBlock.onDidChangeCursorSelection(
  () => {
    const { column, lineNumber } = globalVariable.editorCodeBlock.getPosition();
    globalVariable.editorCodeBlock.setPosition({ lineNumber, column });
  },
);
/* Disable paste option */
globalVariable.editorCodeBlock.onKeyDown((event)=>{
    const {keyCode, ctrlKey, metaKey} = event;
    if((keyCode === 33 || keyCode ===52) && (metaKey || ctrlKey)){
      event.preventDefault();
    }
  });