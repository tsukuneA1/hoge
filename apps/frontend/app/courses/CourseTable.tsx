// app/courses/CoursesTable.tsx
"use client";

import type { ColumnDef } from "@tanstack/react-table";
import { BaseTable } from "@/app/components/BaseTable";
import type { components } from "../utils/api/generated/schema";
import { useQueryStates } from "nuqs";
import { courseSearchParams } from "./searchParams";

type CourseListItem = components["schemas"]["CourseListItem"];

type Props = {
  data: CourseListItem[];
  total: number;
};

const columns: ColumnDef<CourseListItem>[] = [
  {
    accessorKey: "title",
    header: () => (
      <div className="flex flex-row items-center gap-1.5">
        <div>授業名</div>
      </div>
    ),
    meta: {
      headerClass: "flex-1",
      class: "flex-1",
    },
  },
  {
    id: "faculty",
    header: () => (
      <div className="flex flex-row items-center gap-1.5">
        <div>開講学部</div>
      </div>
    ),
    cell: ({ row }) => {
      if (row.original.faculty.length === 0) {
        return "なし";
      }

      return (
        <div className="flex flex-row items-center gap-2">
          {row.original.faculty}
        </div>
      );
    },

    meta: {
      headerClass: "flex-1",
      class: "flex-1",
    },
  },
  {
    id: "term_day_period",
    header: () => (
      <div className="flex flex-row items-center gap-1.5">
        <div>曜日時限</div>
      </div>
    ),
    cell: ({ row }) => {
      if (row.original.term_day_period.length === 0) {
        return "なし";
      }

      return (
        <div className="flex flex-row items-center gap-2">
          {row.original.term_day_period}
        </div>
      );
    },

    meta: {
      headerClass: "flex-1",
      class: "flex-1",
    },
  },
];

export function CoursesTable({ data, total }: Props) {
  const [{ limit, offset }, setParams] = useQueryStates(courseSearchParams);

  const moveToPage = (nextOffset: number) => {
    void setParams(
      {
        offset: nextOffset,
      },
      {
        history: "replace",
        shallow: false
      }
    )
  };

  return (
    <BaseTable
      columns={columns}
      data={data}
      limit={limit}
      offset={offset}
      total={total}
      onClickNextPage={() => moveToPage(offset + limit)}
      onClickPreviousPage={() => moveToPage(offset - limit)}
      onRowClick={(row) => {
        console.log(row);
      }}
      emptyMessage="hogehoge"
      emptyIcon
    />
  );
}
