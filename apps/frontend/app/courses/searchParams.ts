import {
  createSearchParamsCache,
  parseAsInteger,
  parseAsString,
} from "nuqs/server";

export const LIMIT = 10;

export const courseSearchParams = {
  q: parseAsString.withDefault(""),
  limit: parseAsInteger.withDefault(LIMIT),
  offset: parseAsInteger.withDefault(0),
  faculty: parseAsString.withDefault(""),
};

export const courseSearchParamsCache =
  createSearchParamsCache(courseSearchParams);
