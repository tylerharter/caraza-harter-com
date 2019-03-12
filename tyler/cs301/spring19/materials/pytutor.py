import os, sys, json, subprocess
from subprocess import check_output

PYTUTOR = "/Users/trh/git_co/OnlinePythonTutor/v5-unity/generate_json_trace.py"

EMBEDDING = """
<div id="DIV"></div>
<script type="text/javascript">
  var trace = TRACE;
  addVisualizerToPage(trace, 'DIV',  {startingInstruction: 0, hideCode: false, lang: "py3", disableHeapNesting: true});
</script>
"""

def run_pytutor(py):
    try:
        js = check_output(["python", PYTUTOR, py])
    except subprocess.CalledProcessError as e:
        js = e.output
    return json.dumps(json.loads(js))

def main():
    if len(sys.argv) < 2:
        print("Usage: python pytutor.py file1.py [file2.py, ...]")
        sys.exit(1)

    for py in sys.argv[1:]:
        js = run_pytutor(py)
        div = py.replace(".", "_").replace("/", "_")
        code = EMBEDDING.replace("DIV", div).replace("TRACE", js)
        print(code)


if __name__ == '__main__':
     main()
