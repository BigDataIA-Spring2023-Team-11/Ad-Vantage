import json

import streamlit as st
import base64
# from streamlit import SessionState



from api_utils import get_grammer_corrected_text, product_name_generator,\
    ad_from_product_description, generate_image, get_s3_object_url, generate_html, read_html_template_from_s3


with open('config.json', 'r') as f:
    config = json.load(f)
image_dir = config['dir']['image']
if 'image' not in st.session_state:
    st.session_state.image = None
def main():

    st.markdown(
            "<h3 style='text-align: center'><span style='color: #2A76BE;'>AdVantage</span></h3>",
            unsafe_allow_html=True)



    product_description = st.text_input("product_description")
    grammer_corrected_description = get_grammer_corrected_text(product_description)
    adjective = st.text_input("Describe your product in a word or two separated by comma ','")



    if st.button("Get Product Name!"):
            st.markdown(f"{grammer_corrected_description}-------corrected")
            generated_product_name = product_name_generator(grammer_corrected_description,adjective)
            st.markdown(f"{generated_product_name}-------product_name")
    target_customer = st.text_input("Who is your target customer")


    # Add a button to generate the ad
    if st.button("Get Ad!"):
            ad_from_product_desc = ad_from_product_description(target_customer,grammer_corrected_description)
            st.markdown(f"{grammer_corrected_description} ------> grammer corrected")
            st.markdown(f"{ad_from_product_desc}----------ad_from_Desc")



    # Add button to generate image
    chosen_title = st.text_input("Choose a title")

    button_clicked = st.button("Generate Image")

    # If button is clicked, generate and display image
    if button_clicked:
        # Display spinner while image is being generated
        with st.spinner("Generating image..."):
            advert_image = generate_image(grammer_corrected_description,chosen_title)

        # If image is generated successfully, display it
        if advert_image is not None:
            st.image(advert_image, caption='Advertisement Image', use_column_width=True)
            st.session_state.image = advert_image

        # If image generation fails, display error message
        else:
            st.error("Failed to generate image")



    col1,col2 = st.columns([1,1])
    with col1:
        if st.button("Generate link to download image"):
            if st.session_state.image is not None:  # check if an image has been generated
                st.image(st.session_state.image, caption='Advertisement Image', use_column_width=True)
            url = get_s3_object_url(f"{chosen_title}.png")
            with st.expander("Expand for url"):
                st.write(url)
        # html_content = generate_html(chosen_title, product_description, image_dir)
        # with open(f"templates/{chosen_title}.html", "w") as f:
        #     # Write some HTML content to the file
        #     f.write(html_content)
    # with col2:
    st.markdown("---------------------------------------------------------------------------------------------------------")
    st.markdown(
        "<h3 style='text-align: center'><span style='color: #2A76BE;'>Get started with a website for your product</span></h3>",
        unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,1,1])
    with c2:
        if st.button('Download my website'):
            image_dir1 = get_s3_object_url(f"{chosen_title}.png")
            generate_html(chosen_title, product_description, image_dir1)
            # Write the HTML to a file or display it in a Streamlit component
            # For example, to display it in Streamlit:
            with open(f'templates/{chosen_title}.html', 'r') as f:
                file_contents = f.read()
                b64 = base64.b64encode(file_contents.encode()).decode()
                href = f'<a href="data:file/html;base64,{b64}" download="{chosen_title}.html">Download file</a>'
                with st.expander("Expand for url"):
                    st.write(href, unsafe_allow_html=True)

    #
    # if st.button("Get html code from api"):
    #     image_url = get_s3_object_url(f"{chosen_title}.png")
    #     # image_url = f"generated_images/{chosen_title}.png"
    #     st.markdown(f"{image_url} ------> image url")
    #     st.markdown(f'{chosen_title.replace("_"," ")} ------> title')
    #     st.markdown(f"{grammer_corrected_description} ------> grammar corrected")
    #
    #     code = generate_html(image_url,chosen_title.replace("_"," "),grammer_corrected_description)
    #     st.markdown(code)


if __name__ == "__main__":
    main()