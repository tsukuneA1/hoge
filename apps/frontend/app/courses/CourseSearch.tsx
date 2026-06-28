"use client";

import { debounce, useQueryStates } from "nuqs";
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { courseSearchParams } from "./searchParams";

const faculties = [
  "指定なし",
  "政治経済学部",
  "法学部",
  "教育学部",
  "商学部",
  "社会科学部",
  "人間科学部",
  "スポーツ科学部",
  "国際教養学部",
  "文化構想学部",
  "文学部",
  "人間科学部（通信教育課程）",
  "基幹理工学部",
  "創造理工学部",
  "先進理工学部",
  "政治経済学研究科",
];

export const CourseSearch = () => {
  const [{ q, faculty }, setParams] = useQueryStates(courseSearchParams);

  const changeKeyword = (value: string) => {
    void setParams(
      {
        q: value === "" ? null : value,
        offset: 0,
      },
      {
        history: "replace",
        shallow: false,
        limitUrlUpdates: debounce(400),
      },
    );
  };

  const changeFaculty = (value: string) => {
    void setParams(
      {
        faculty: value === faculties[0] ? null : value,
        offset: 0,
      },
      {
        history: "replace",
        shallow: false,
      },
    );
  };

  return (
    <FieldGroup className="flex flex-row gap-2">
      <Field>
        <FieldLabel htmlFor="input-field-keyword">検索キーワード</FieldLabel>
        <Input
          id="input-field-keyword"
          type="text"
          value={q}
          onChange={(e) => changeKeyword(e.target.value)}
        />
      </Field>
      <Field>
        <FieldLabel htmlFor="select-field-faculty">対象学部</FieldLabel>
        <Select
          value={faculty === "" ? faculties[0] : faculty}
          onValueChange={changeFaculty}
        >
          <SelectTrigger id="select-field-faculty">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {faculties.map((faculty) => (
              <SelectItem key={faculty} value={faculty}>
                {faculty}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </Field>
    </FieldGroup>
  );
};
