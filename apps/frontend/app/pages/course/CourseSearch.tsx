"use client";

import InputField from "@/app/components/InputField"
import { useRouter, useSearchParams } from "next/navigation"
import { useState } from "react"

export const CourseSearch = () => {
    const router = useRouter()
    const searchParams = useSearchParams();

    const [keyword, setKeyword] = useState("")

    const changeKeyword = (value: string) => {
        setKeyword(value)
        const params = new URLSearchParams(searchParams.toString());
        if (keyword === ""){
            params.delete("q")
        } else {
            params.set("q", value)
            params.set("offset", "0")
        }

        router.push(`course?${params.toString()}`);
    }

    return (
        <div className="flex items-center gap-4">
            <InputField
                placeholder="検索キーワード"
                value={keyword}
                onChange={changeKeyword}
            />
        </div>
    )
}