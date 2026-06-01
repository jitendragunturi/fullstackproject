"use client";

import { useState } from "react";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import clsx from "clsx";
import type { Card } from "@/lib/kanban";

type KanbanCardProps = {
  card: Card;
  onDelete: (cardId: string) => void;
};

export const KanbanCard = ({ card, onDelete }: KanbanCardProps) => {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: card.id });
  const [expanded, setExpanded] = useState(false);

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <article
      ref={setNodeRef}
      style={style}
      className={clsx(
        "rounded-2xl border border-transparent bg-white px-4 py-4 shadow-[0_12px_24px_rgba(3,33,71,0.08)]",
        "transition-all duration-150",
        isDragging && "opacity-60 shadow-[0_18px_32px_rgba(3,33,71,0.16)]"
      )}
      {...attributes}
      {...listeners}
      data-testid={`card-${card.id}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <h4 className="font-display text-base font-semibold text-[var(--navy-dark)]">
            {card.title}
          </h4>
          <p className="mt-2 text-sm leading-6 text-[var(--gray-text)] truncate">
            {card.details}
          </p>
        </div>
        <div className="flex flex-col items-end gap-2">
          <button
            type="button"
            onClick={() => setExpanded(true)}
            className="rounded-full border border-transparent bg-[var(--surface)] px-2 py-1 text-xs font-semibold text-[var(--navy-dark)] transition hover:border-[var(--stroke)]"
            aria-label={`View ${card.title}`}
          >
            View
          </button>
          <button
            type="button"
            onClick={() => onDelete(card.id)}
            className="rounded-full border border-transparent px-2 py-1 text-xs font-semibold text-[var(--gray-text)] transition hover:border-[var(--stroke)] hover:text-[var(--navy-dark)]"
            aria-label={`Delete ${card.title}`}
          >
            Remove
          </button>
        </div>
      </div>

      {expanded ? (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center"
        >
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setExpanded(false)}
          />
          <div className="relative z-10 w-[min(720px,90%)] rounded-2xl bg-white p-6 shadow-xl">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-xl font-semibold text-[var(--navy-dark)]">
                  {card.title}
                </h3>
                <p className="mt-3 text-sm text-[var(--gray-text)] whitespace-pre-wrap">
                  {card.details}
                </p>
              </div>
              <div className="ml-4 flex-shrink-0">
                <button
                  onClick={() => setExpanded(false)}
                  className="rounded-md bg-[var(--surface)] px-3 py-2 text-sm font-semibold"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </article>
  );
};
