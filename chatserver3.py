from flask import Flask, request, render_template_string ,render_template
import openai
import os

app = Flask(__name__)

openai.api_key = "" 
os.environ['OPENAI_API_KEY'] = openai.api_key

task_exp = '''
# 指示
あなたは人の意見を論理的に否定しなければならない立場になりました。
あなたの職業は何でも構いませんので、どれか一つになりきり、その人の立場から出された意見に対して論理的に否定してください。

# 出力形式
以下のような形式で「入力された意見」を「ある職業の立場」で、「否定する」ことを数回記述し、辞書形式でまとして下さい。
例えば、「入力された意見」が"学校のテストは必要ある"となっているとき、無作為に職業から一つ選び、ここでは「ある職業の立場」として医者が選択されたとします。
「否定する」とは"学校のテストは必要ではない"を否定する意見を出すことであり、医者の立場では、
"患者の病態を知るために医学を勉強するが、暗記能力をつけるために、学校でテストをしっかりすべきだ。"という論理的な意見が一つとして考えられ、
それを
{"job_value":"医者","negative_value":"患者の病態を知るために医学を勉強するが、暗記能力をつけるために、学校でテストをしっかりすべきだ。"}
のように出力する。
ここでは入力する意見に対して入力された意見に加えて無作為で職業を選び、合計5つの立場で考える。
また、入力された意見、ある職業の立場、否定の意見を出力するときは改行してほしい
また、もう一度読み込んだ際、被らないように職業はランダムにすること。
'''
client = openai.OpenAI()
model_name = "gpt-3.5-turbo"
isresponse=True

@app.route('/')
def index():
    return render_template("chatframeLast.html")

@app.route('/submit_opinion', methods=['POST'])
def submit_opinion():
    if request.method == 'POST':
        opinion_user = request.form['opinion']
        list_pro = request.form['professions'].split()

        response = client.chat.completions.create(
            model=model_name,
            temperature=0,
            messages=[
                {"role": "system", "content": task_exp},
                {"role": "user", "content": f"以下の意見から論理的に否定するものを考えてください。また、にユーザーが入力した職業である{list_pro}に加えて、無作為で職業を選び、合計5つの職業で考えてください\n---\n{opinion_user}"}
            ]
        )
        current_response = response.choices.pop().message.content

        # レスポンスを解析してリストに変換
        items = []
        for line in current_response.split('\n'):
            if line.startswith('{') and line.endswith('}'):
                item = eval(line)  # 辞書形式の文字列を辞書に変換
                items.append(item)

        # index2.htmlにデータを渡す
        return render_template('chatframe5.html', opinion_user=opinion_user, items=items)


if __name__ == '__main__':
    app.run(debug=True)