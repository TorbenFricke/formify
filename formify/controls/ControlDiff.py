from formify.controls import ControlHtml

template= """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<title></title>
	<style type="text/css">
		body {
			background-color: #fcfcfc;
		}

		table.diff {
			background-color: white;
			font-family: monospace; 
			width: 100%;

			border-collapse: separate;
			border:solid #ccc 1px;
			border-radius:6px;
		}

		tbody:not(:first-of-type) > tr:first-child > td {
			border-top:solid #ccc 1px;
		}

		.diff_header {
			background-color:#0058920d; 
			color: #064063;
			width: 2px;
		}
		td.diff_header {text-align:right}
		.diff_next {
			background-color:#0058920d;
			width: 2px;
		}
		.diff_add {
			background-color:#d5efd5;
			border-radius: 3px;
			border: 1px solid #7bd47b;
		}
		.diff_chg {
			background-color:#ffffad;
			border-radius: 3px;
			border: 1px solid #e2e25f;
		}
		.diff_sub {
			background-color:#f3bbac;
			border-radius: 3px;
			border: 1px solid #e25353;
		}

		tr:nth-child(3n) {
			max-width: 200px;
			overflow: scroll;
		}

		.diff_next>a {
			color: #f0f3f5;
			text-decoration: none;
		}

		colgroup {border: none;}
	</style>
</head>

<body>
<div class="wrapper">
{{diff}}
</div>
</body>

</html>
"""


def compare(lines1, lines2, **kwargs):
	import difflib
	return template.replace(
			"{{diff}}",
			difflib.HtmlDiff().make_table(lines1, lines2,
				context=kwargs.pop("context", True), **kwargs)
		)


class ControlDiff(ControlHtml):
	def get_value(self):
		try:
			return self._data
		except:
			pass
		return None

	def set_value(self, value):
		self.control.setHtml(compare(value[0], value[1]))
