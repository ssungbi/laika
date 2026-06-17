var fso = new ActiveXObject("Scripting.FileSystemObject");
var file = fso.OpenTextFile("c:/Users/SB/Desktop/연습용/script.js", 1);
var jsCode = file.ReadAll();
file.Close();

try {
    eval(jsCode);
    WScript.Echo("Syntax OK!");
} catch (e) {
    WScript.Echo("Error: " + e.message);
    WScript.Echo("Line: " + e.line);
}
