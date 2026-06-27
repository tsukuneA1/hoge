"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const faculties = [
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
  const router = useRouter();
  const searchParams = useSearchParams();

  const [keyword, setKeyword] = useState<string>();
  const [faculty, setFaculty] = useState<string>();

  const changeKeyword = (value: string) => {
    setKeyword(value);
    const params = new URLSearchParams(searchParams.toString());
    if (value === "") {
      params.delete("q");
    } else {
      params.set("q", value);
      params.set("offset", "0");
    }

    router.push(`courses?${params.toString()}`);
  };

  const changeFaculty = (value: string) => {
    setFaculty(value);
    const params = new URLSearchParams(searchParams.toString());
    if (value === "") {
      params.delete("faculty");
    } else {
      params.set("faculty", value);
      params.set("offset", "0");
    }

    router.push(`courses?${params.toString()}`);
  };

  return (
    <FieldGroup className="flex flex-row gap-2">
      <Field>
        <FieldLabel htmlFor="input-field-keyword">検索キーワード</FieldLabel>
        <Input
          id="input-field-keyword"
          type="text"
          value={keyword}
          onChange={(e) => {
            changeKeyword(e.target.value);
          }}
        />
      </Field>
      <Field>
        <FieldLabel>対象学部</FieldLabel>
        <Select value={faculty} onValueChange={(value) => changeFaculty(value)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {faculties.map((faculty) => {
              return <SelectItem value={faculty}>{faculty}</SelectItem>;
            })}
          </SelectContent>
        </Select>
      </Field>
    </FieldGroup>
  );
};
