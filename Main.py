    goals = []
    if weight_loss:
        goals.append("Weight loss")
        fat_range = st.slider('Fat (g)', min_value=0, max_value=50, value=(0, 35))
        protein_range = st.slider('Protein (g)', min_value=0, max_value=50, value=(0, 56))
        carb_range = st.slider('Carbohydrates (g)', min_value=0, max_value=100, value=(0, 150))

    if weight_gain:
        goals.append("Weight gain")
        fat_range = st.slider('Fat (g)', min_value=0, max_value=50, value=(0, 40))
        protein_range = st.slider('Protein (g)', min_value=0, max_value=200, value=(0, 136))
        carb_range = st.slider('Carbohydrates (g)', min_value=0, max_value=300, value=(0, 195))
    if maintenance:
        goals.append("Maintenance")
        fat_range = st.slider('Fat (g)', min_value=0, max_value=50, value=(0, 15))
        protein_range = st.slider('Protein (g)', min_value=0, max_value=200, value=(0, 75))
        carb_range = st.slider('Carbohydrates (g)', min_value=0, max_value=300, value=(0, 163))

    if rapid_weight_loss:
        goals.append("Rapid Weight Loss")
        fat_range = st.slider('Fat (g)', min_value=0, max_value=50, value=(0, 25))
        protein_range = st.slider('Protein (g)', min_value=0, max_value=200, value=(0, 113))
        carb_range = st.slider('Carbohydrates (g)', min_value=0, max_value=200, value=(0, 100))
