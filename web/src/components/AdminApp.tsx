"use client";

import jsonServerProvider from "ra-data-json-server";
import { Admin, EditGuesser, ListGuesser, Resource } from "react-admin";

const dataProvider = jsonServerProvider("https://jsonplaceholder.typicode.com");

const AdminApp = () => (
	<Admin dataProvider={dataProvider}>
		<Resource
			name="users"
			list={ListGuesser}
			edit={EditGuesser}
			recordRepresentation="name"
		/>
		<Resource
			name="posts"
			list={ListGuesser}
			edit={EditGuesser}
			recordRepresentation="title"
		/>
		<Resource name="comments" list={ListGuesser} edit={EditGuesser} />
	</Admin>
);

export default AdminApp;
