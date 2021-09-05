from sqlalchemy.engine.interfaces import ExceptionContext
from source import ElasticResponse, read_query
from generator.search import templatize
from datetime import datetime, timedelta
from gramex.transforms import handler
from generator.utils import load_spacy_model
import yaml


nlp = load_spacy_model()


@handler
def tree(*args):
    return [
        {
            "domainName": "backup",
            "objectives": [
                {
                    "policy_complaint": [
                        "policy_changes",
                        "backup_copies",
                        "retention_status",
                    ]
                },
                {"job_failure": []},
            ],
        },
        {"domainName": "incident", "objectives": []},
    ]


def collect(handler):
    html_elements = """<p><strong>Retention Policy Status:&nbsp;</strong></p>
        <p>&nbsp;</p>
        <p><strong>Summary</strong>: This section describes the discrepancies in the backup retention policies created on the server.&nbsp;&nbsp;</p>
        <p>&nbsp;</p>
        <p><strong>Description</strong>: There are three different statuses (Warning, Critical, and Complaint).</p>
        <p>&nbsp;</p>
        <p>*&nbsp;&nbsp;<em>Critical</em>: Retention policy does not exist on the server but will be available in the document.</p>
        <p>* <em>Warning</em>: Retention policy exists on the server but will not be available in the document.</p>
        <p>* <em>Complaint</em>: It adheres to the policy.</p>
        <p>&nbsp;</p>
        <table>
        <tbody>
        <tr>
        <td width="149">
        <p>Host Name</p>
        </td>
        <td width="149">
        <p>&nbsp;Critical</p>
        </td>
        <td width="149">
        <p>Warning</p>
        </td>
        <td width="149">
        <p>Complaint</p>
        </td>
        </tr>
        <tr>
        <td width="149">
        <p>MRS-IS-00021</p>
        </td>
        <td width="149">
        <p>3</p>
        </td>
        <td width="149">
        <p>20</p>
        </td>
        <td width="149">
        <p>150</p>
        </td>
        </tr>
        <tr>
        <td width="149">
        <p>MRS-IS-00021</p>
        </td>
        <td width="149">
        <p>1</p>
        </td>
        <td width="149">
        <p>40</p>
        </td>
        <td width="149">
        <p>400</p>
        </td>
        </tr>
        </tbody>
        </table>
        <p>&nbsp;</p>
        <p>Note: Sort it by health score and limit it to 5 entries only. Health score will be calculated based on the Bayesian avg.</p>
        <p><span style="text-decoration: line-through;">&nbsp;</span></p>
        <table>
        <tbody>
        <tr>
        <td width="66">
        <p>Health</p>
        </td>
        <td width="535">
        <table>
        <tbody>
        <tr>
        <td width="106">
        <p>Red</p>
        </td>
        <td width="414">
        <p>Server2, Server3</p>
        </td>
        </tr>
        <tr>
        <td width="106">
        <p>Amber</p>
        </td>
        <td width="414">
        <p>Server33, Server11</p>
        </td>
        </tr>
        <tr>
        <td width="106">
        <p>Green</p>
        </td>
        <td width="414">
        <p>Server10, Server10, Server10, Server10</p>
        </td>
        </tr>
        </tbody>
        </table>
        </td>
        </tr>
        </tbody>
        </table>
        <p>&nbsp;</p>
        <p>Health &ndash; Green: SERVER24 [Threshold: Critical =0 , Warning &lt; 50% ]</p>
        <p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;Red: SERVER1 (CRTICAL &ndash; 10% &amp;&amp; WARING &ndash; 25%) [Threshold: Critical &gt;0]</p>
        <p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;Amber: [Threshold: Critical =0 , Warning &gt; 50% ]</p>
        <p>&nbsp;</p>
        <p><strong>Prescriptive</strong>: By identifying the critical polices (Red) user can create those policies on the server.</p>
        <p>&nbsp;</p>
        <p><strong>Policy changes:&nbsp;</strong></p>
        <p><strong>Summary: </strong><strong>Policy Change</strong>&nbsp;provides the information about the policy changed date on a particular backup server by the respective backup admin. This accounts for the changes that happened during the last 10 days.</p>
        <p><strong>Description</strong> :&nbsp;</p>
        <p><span style="text-decoration: line-through;">For the backup server MRS-IS-00021, the changes happened on Jun 29, 2020, @ 05:30:00.000 to the management class MC_SHD_SQL_15DAY of the domain DO_SQL by DEV345.</span></p>
        <table>
        <tbody>
        <tr>
        <td width="150">
        <p><strong>Host Name</strong></p>
        </td>
        <td width="879">
        <p>&nbsp;</p>
        </td>
        </tr>
        <tr>
        <td width="150">
        <p><strong>MRS-IS-00021</strong><strong>&nbsp; </strong><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</strong></p>
        </td>
        <td width="879">
        <table>
        <tbody>
        <tr>
        <td width="111">
        <p>Jan 14</p>
        </td>
        <td width="123">
        <p>DO SQL</p>
        </td>
        <td width="441">
        <p>MC_SHD_SQL_LARGE</p>
        </td>
        <td width="187">
        <p>ADMIN</p>
        </td>
        </tr>
        <tr>
        <td width="111">
        <p>Jan 29</p>
        </td>
        <td width="123">
        <p>DO SQL</p>
        </td>
        <td width="441">
        <p>MC_SHD_SQL_15DAY,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;</p>
        <p>MC_SHD_SQL_22DAY</p>
        </td>
        <td width="187">
        <p>DEV345</p>
        </td>
        </tr>
        <tr>
        <td width="111">
        <p>Oct 25</p>
        </td>
        <td width="123">
        <p>DO SQL</p>
        </td>
        <td width="441">
        <p>MC_SHD_SQL_22DAY</p>
        </td>
        <td width="187">
        <p>DEV345</p>
        </td>
        </tr>
        </tbody>
        </table>
        </td>
        </tr>
        <tr>
        <td width="150">
        <p><strong>MRS-IS-00025 </strong><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</strong></p>
        </td>
        <td width="879">
        <table width="863">
        <tbody>
        <tr>
        <td width="111">
        <p>Jan 14</p>
        </td>
        <td width="124">
        <p>DO SQL</p>
        </td>
        <td width="441">
        <p>MC_SHD_SQL_LARGE&nbsp;&nbsp;</p>
        </td>
        <td width="187">
        <p>ADMIN</p>
        </td>
        </tr>
        <tr>
        <td width="111">
        <p>Jan 29</p>
        </td>
        <td width="124">
        <p>DO SQL</p>
        </td>
        <td width="441">
        <p>MC_SHD_SQL_15DAY, &nbsp;&nbsp;&nbsp;</p>
        <p>MC_SHD_SQL_22DAY</p>
        </td>
        <td width="187">
        <p>DEV345</p>
        </td>
        </tr>
        <tr>
        <td width="111">
        <p>Oct 25</p>
        </td>
        <td width="124">
        <p>DO SQL</p>
        </td>
        <td width="441">
        <p>MC_SHD_SQL_22DAY</p>
        </td>
        <td width="187">
        <p>DEV345</p>
        </td>
        </tr>
        </tbody>
        </table>
        </td>
        </tr>
        </tbody>
        </table>
        <p>&nbsp;</p>
        <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>
        <p>&nbsp;</p>

        <p>&nbsp; Note: Set some criteria to show top 4/5 server details only. Sorting Criteria &ndash; active servers, production servers, no. of changes e.t.c</p>
        """
    return {"data":html_elements}
    data = ElasticResponse()
    params = handler.argparse(
        from_timestamp={
            "type": str,
            "default": (datetime.utcnow() - timedelta(weeks=10)).isoformat(),
        },
        to_timestamp={"type": str, "default": datetime.utcnow().isoformat()},
        data={"type": bool, "default": False},
    )
    sql_query = read_query("backup", *handler.path_args)
    respose_body = {}
    respose_body["objective"] = handler.path_args[0]
    respose_body["subject"] = handler.path_args[1]
    respose_body["data"] = data.get_response(sql_query, params)
    
    # respose_body["narrative"] =[{
    #         "type": "Policy Changes",
    #         "text": """<ul><li>Summary : <li> <li>\nDescriptive :<li> <li>\nPredictive : <li></ul>""",
    #         "header": "policy_changes",
    #     },
    #     {
    #         "type": "Backup Copies",
    #         "text":  "<ul><li>Summary :<li> <li>\nDescriptive :<li> <li>\nPredictive :<li></ul>",
    #         "header": "backup_copies",
    #     },
    #     {
    #         "type": "Retention Status",
    #         "text":  "<ul><li>Summary : <li> <li>\n<b>Descriptive :<li> <li>\nPredictive :<li></ul>",
    #         "header": "retention_status",
    #     }]


    # respose_body["narrative"] = [
    #     {
    #         "type": "summary",
    #         "text": "some narrative text goes here.",
    #         "header": "Summary",
    #     },
    #     {
    #         "type": "descriptive",
    #         "text": "some narrative text goes here.",
    #         "header": "insights",
    #     },
    #     {
    #         "type": "prescriptive",
    #         "text": "some narrative text goes here.",
    #         "header": "Recommendation",
    #     },
    #     {
    #         "type": "predictive",
    #         "text": "some narrative text goes here.",
    #         "header": "Forcast",
    #     },
    # ]
    try:
        print('Inside try block')
        text = "You can view summary information about backups created by backup copy jobs. The summary information provides the Host Name and the aggregated sum of days. There are total 4 backup servers out of which MRS-IS-00023 has the least number of the total sum, which is 3.0"
        # text = nlp(text)
        # nugget = templatize(text, {"_sort": ["-Days"]} , respose_body["data"])
        # rendered_text = nugget.render(respose_body["data"])
        # print("**"*10,rendered_text)
        # respose_body["narrative"]['summary'] = rendered_text
        respose_body["narrative"][1]['text'] = f"<ul><li>Summary : {text}<li> <li>\nDescriptive :<li><li>\nPredictive :<li></ul>"
        return respose_body

    except BaseException as e:
       print(e)
    if not params["data"]:
        respose_body["data"] = []
    return respose_body


def get_objectives(domain):
    with open(domain + "_queries.yaml", "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


@handler
def objectives(*args):
    return get_objectives("backup")


def get_subjects(domain, objective):
    with open(domain + "_queries.yaml", "r") as stream:
        try:
            res = yaml.safe_load(stream)
            if not res.get(objective):
                return get_objectives("backup")
            return res.get(objective)
        except yaml.YAMLError as exc:
            print(exc)


@handler
def subjects(*args):
    return get_subjects("backup", *args)


if __name__ == "__main__":
    pass

name=""