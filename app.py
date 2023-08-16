import dash
import dash_bootstrap_components as dbc


app = dash.Dash(
    "Swimming Atlet",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server
app.config.suppress_callback_exceptions = True
app.title = "Swimming Club"
app.description = """A dashboard to display price indicators for Bitcoin, 
                  Ethereum, Ripple, and Bitcoin-cash."""


########################################################################
#
#  For Google Analytics
#
########################################################################
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-15C7GNBCP3"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        
          gtag('config', 'G-15C7GNBCP3');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta property="og:type" content="article">
        <meta property="og:title" content="Cryptocurrency Indicators Dashboard"">
        <meta property="og:site_name" content="https://crypto-indicators-dashboard.herokuapp.com">
        <meta property="og:url" content="https://crypto-indicators-dashboard.herokuapp.com">
        <meta property="og:image" content="https://raw.githubusercontent.com/dc-aichara/DS-ML-Public/master/Medium_Files/dashboard_demo/assets/favicon.ico">
        <meta property="article:published_time" content="2020-11-01">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""
