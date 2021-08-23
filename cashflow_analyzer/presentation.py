from matplotlib import pyplot as plt
from collections import namedtuple
from cashflow_analyzer.transactions import SCHEMA

Model = namedtuple("Model", "fig_size, amount, x_axis, x_label, y_label, title, color")


def grouped_interface(data, transaction_type, step):
    step_title = "years" if step == "yearly" else "months"
    type_transactions = "cashflow" if transaction_type == "all" else transaction_type

    for payer in data[SCHEMA["payer"]].unique():
        df = data[data[SCHEMA["payer"]] == payer]
        x_axis = df[step_title] if step == "yearly" else df["years"].astype(str) + "-" + df["month"].astype(str)

        yield Model(fig_size=(10, 5),
                    amount=df[SCHEMA["amount"]],
                    x_axis=x_axis,
                    x_label=step_title,
                    y_label=f"{type_transactions} in euro",
                    title=f"{type_transactions} over the {step_title} for {payer}",
                    color=chose_color(type_transactions))


def chose_color(type_transactions):
    if type_transactions == "revenues":
        color = "green"
    elif type_transactions == "expenses":
        color = "red"
    else:
        color = "blue"
    return color


def graph_interface(data, transaction_type, step):
    step_title = "years" if step == "yearly" else "months"
    type = "cashflow" if transaction_type == "all" else transaction_type
    x_axis = data[step_title] if step == "yearly" else data["years"].astype(str) + "-" + data["months"].astype(str)

    return Model(fig_size=(10, 5),
                 amount=data[SCHEMA["amount"]],
                 x_axis=x_axis,
                 x_label=step_title,
                 y_label=f"{type} in euro",
                 title=f"{type} over the {step_title}",
                 color=chose_color(type))


def plot_report(model: Model):
    fig, ax = plt.subplots(figsize=model.fig_size, tight_layout=True)
    ax.plot(model.x_axis, model.amount, '-X')
    ax.set_xlabel(model.x_label)
    ax.set_ylabel(model.y_label)
    ax.set_title(model.title)
    plt.grid()
    plt.xticks(model.x_axis, rotation='vertical')
    return fig


def to_pdfs(models, path):
    from matplotlib.backends.backend_pdf import PdfPages
    with PdfPages(path) as pdf:
        for model in models:
            pdf.savefig(plot_report(model))
            plt.close()
