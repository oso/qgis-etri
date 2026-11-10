def first_point(item):
    element = item.path().elementAt(0)
    return element.x, element.y


def test_categories_are_drawn_between_their_limits(make_window):
    window = make_window("ticino")
    scene = window.graph_plot.scene()
    model = scene.model
    limits = ['worst'] + model.profiles + ['best']

    assert len(scene.category_items) == len(model.categories) == 3
    for i, category in enumerate(model.categories):
        # The category path starts with its upper limit
        upper = scene.profiles_items[limits[i + 1]]
        assert first_point(scene.category_items[category]) \
            == first_point(upper)
