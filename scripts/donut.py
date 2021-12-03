import matplotlib.pyplot as plt


def make_donut_chart(display_data):
    labels = ['Five star', 'Four star', 'Three star', 'Two star', 'One star']

    sizes = [display_data['five-percentage'], display_data['four-percentage'], display_data['three-percentage'],
             display_data['two-percentage'],
             display_data['one-percentage']]

    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#68d9df']

    # plt.pie(sizes, labels=labels, autopct='%1.0f%%', shadow=False, startangle=90, colors=colors, radius=0.85,
    #         pctdistance=0.75)
    #
    # circle = plt.Circle((0, 0), 0.5, color='black', fc='white', linewidth=0)
    #
    # donut = plt.gcf()
    # donut.gca().add_artist(circle)
    # donut.set_size_inches(4, 4)
    #
    # plt.axis('equal')
    # plt.tight_layout()
    # plt.savefig('/home/wappnet-10/workspace_test_learn/sales_stock_prediction/base/static/adminResources/image/plot')
    #
    # plt.close()
