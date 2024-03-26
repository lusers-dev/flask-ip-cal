import re
import netaddr
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "this-secret-is-for-flask-fcc4901b8046255f1591e982be51fc3d"
template_file = 'templates/cal_out'


def replace_words(base_text, body_values):
    for key, val in list(body_values.items()):
        base_text = base_text.replace(key, val)
    return base_text


@app.route("/", methods=['POST', 'GET'])
def process():
    output = None
    entry = None
    try:
        entry = str(request.form['cidr_entry'])
    except Exception as e:
        pass

    ip_net = None
    if entry:
        try: 
            if re.match("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\/[0-9]+$", entry):
                ip_net = netaddr.IPNetwork(entry)

                body = {}
                body["##subnet_id##"] = str(ip_net.network)
                body["##cidr##"] = str(ip_net.cidr)
                body["##prefix##"] = str(ip_net.prefixlen)
                body["##size##"] = str(ip_net.size)
                body["##subnet_mask##"] = str(ip_net.netmask)
                body["##broadcast##"] = str(ip_net.broadcast)
                body["##wildcard_mask##"] = str(ip_net.hostmask)
                body["##gateway_addr##"] = str(ip_net[1])

                try:
                    t = open(template_file, 'r')
                    tempstr = t.read()
                    t.close()

                    output = replace_words(tempstr, body)
                    flash(output)

                except Exception as e:
                    flash(e)
                    pass

            else:
                flash('Invalid CIDR format')
      
        except Exception as e:
            flash(e)
            pass

    return render_template("index.html")


