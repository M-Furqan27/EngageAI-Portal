import requests
import streamlit as st


API_BASE_URL = st.secrets.get(
    "API_BASE_URL",
    "https://engageai-portal.onrender.com",
)


ORGANIZATION_ID = (
    "3fa85f64-5717-4562-b3fc-2c963f66afa6"
)


REQUEST_TIMEOUT = 120


st.set_page_config(
    page_title="Representative Module",
    page_icon="👥",
    layout="wide",
)


st.title("Representative Management")
st.caption(
    "Add and manage company representatives."
)



def get_error_message(response):

    try:
        data = response.json()

        detail = data.get(
            "detail",
            data,
        )

        if isinstance(detail, str):
            return detail

        return str(detail)

    except ValueError:
        return (
            response.text
            or "Unexpected backend error."
        )



def fetch_representatives():

    try:

        response = requests.get(
            f"{API_BASE_URL}/representatives",
            params={
                "organization_id": ORGANIZATION_ID,
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()


    except requests.RequestException as error:

        st.error(
            f"Could not load representatives: {error}"
        )

        return []



def check_calendar_status(
    representative_id: str,
):

    try:

        response = requests.get(
            f"{API_BASE_URL}/representatives/{representative_id}/calendar/check",
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()


    except requests.RequestException as error:

        return {
            "calendar_connected": False,
            "connection_status": "Unknown",
            "error": str(error),
        }



def add_representative(
    representative_name,
    service,
    service_description,
    company_email,
):

    payload = {

        "organization_id":
            ORGANIZATION_ID,

        "representative_name":
            representative_name,

        "service":
            service,

        "service_description":
            service_description,

        "company_email":
            company_email,
    }


    try:

        response = requests.post(
            f"{API_BASE_URL}/representatives",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )


        if response.status_code == 201:

            return (
                True,
                "Representative added successfully."
            )


        return (
            False,
            get_error_message(response)
        )


    except requests.RequestException as error:

        return (
            False,
            str(error)
        )



def delete_representative(
    representative_id,
):

    try:

        response = requests.delete(
            f"{API_BASE_URL}/representatives/{representative_id}",
            timeout=REQUEST_TIMEOUT,
        )


        if response.status_code == 204:

            return True


        return False


    except requests.RequestException:

        return False





with st.form(
    "add_representative_form",
    clear_on_submit=True,
):

    st.subheader(
        "Add Representative"
    )


    representative_name = st.text_input(
        "Representative Name",
        placeholder="Ali",
    )


    service = st.text_input(
        "Service",
        placeholder="Vehicle Inspection",
    )


    service_description = st.text_area(
        "Service Description",
        placeholder=(
            "Describe the service provided..."
        ),
    )


    company_email = st.text_input(
        "Company Email",
        placeholder="ali@company.com",
    )


    submitted = st.form_submit_button(
        "Add Representative",
        use_container_width=True,
    )


    if submitted:


        if not representative_name.strip():

            st.error(
                "Representative name is required."
            )


        elif not service.strip():

            st.error(
                "Service is required."
            )


        elif not service_description.strip():

            st.error(
                "Service description is required."
            )


        elif not company_email.strip():

            st.error(
                "Company email is required."
            )


        else:

            success, message = add_representative(
                representative_name.strip(),
                service.strip(),
                service_description.strip(),
                company_email.strip(),
            )


            if success:

                st.success(message)

                st.rerun()


            else:

                st.error(message)



st.divider()


st.subheader(
    "Representatives"
)



representatives = fetch_representatives()



if not representatives:

    st.info(
        "No representatives added yet."
    )


else:


    for representative in representatives:


        representative_id = (
            representative[
                "representative_id"
            ]
        )


        # Check real Google status
        calendar_status = check_calendar_status(
            representative_id
        )


        connection_status = (
            calendar_status.get(
                "connection_status",
                "Unknown",
            )
        )



        with st.container(border=True):


            col1, col2, col3, col4, col5, col6, col7 = st.columns(
                [
                    1.2,
                    1.2,
                    1.5,
                    2,
                    1.2,
                    1.2,
                    0.8,
                ]
            )


            with col1:

                st.write(
                    "**Representative**"
                )

                st.write(
                    representative.get(
                        "representative_name",
                        "Unknown",
                    )
                )


            with col2:

                st.write(
                    "**Service**"
                )

                st.write(
                    representative.get(
                        "service",
                        "",
                    )
                )


            with col3:

                st.write(
                    "**Email**"
                )

                st.write(
                    representative.get(
                        "company_email",
                        "",
                    )
                )


            with col4:

                st.write(
                    "**Description**"
                )

                st.write(
                    representative.get(
                        "service_description",
                        "",
                    )
                )


            with col5:

                st.write(
                    "**Invitation**"
                )


                invitation = representative.get(
                    "invitation_status",
                    "Pending",
                )


                if invitation == "Sent":

                    st.success(
                        "Sent"
                    )

                elif invitation == "Email Failed":

                    st.error(
                        "Failed"
                    )

                else:

                    st.warning(
                        invitation
                    )



            with col6:

                st.write(
                    "**Calendar**"
                )


                if connection_status == "Connected":

                    st.success(
                        "Connected"
                    )


                elif connection_status == "Revoked":

                    st.error(
                        "Revoked"
                    )


                else:

                    st.warning(
                        "Not Connected"
                    )



            with col7:

                st.write(
                    "**Action**"
                )


                if st.button(
                    "Delete",
                    key=f"delete_{representative_id}",
                    use_container_width=True,
                ):

                    if delete_representative(
                        representative_id
                    ):

                        st.success(
                            "Deleted successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Delete failed."
                        )