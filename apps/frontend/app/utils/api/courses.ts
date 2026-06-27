import { apiClient } from "./client";

export type ListCoursesParams = {
	academicYear: number;
	q?: string;
	limit?: number;
	offset?: number;
};

export async function listCourses(params: ListCoursesParams) {
	const { data, error } = await apiClient.GET("/courses", {
		params: {
			query: {
				academic_year: params.academicYear,
				q: params.q || undefined,
				limit: params.limit ?? 20,
				offset: params.offset ?? 0,
			},
		},
	});

	if (error) {
		throw new Error("Failed to list courses");
	}

	return data;
}

export async function getCourse(pkey: string) {
	const { data, error, response } = await apiClient.GET("/courses/{pkey}", {
		params: {
			path: { pkey },
		},
	});

	if (response.status === 404) {
		return null;
	}

	if (error) {
		throw new Error("Failed to get course");
	}

	return data;
}
