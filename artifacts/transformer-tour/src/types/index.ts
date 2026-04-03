export interface BlockData {
  id: string;
  name: string;
  nameIgbo: string;
  description: string;
  descriptionIgbo: string;
  position: [number, number, number];
  color: number;
}

export interface ArchitectureData {
  name: string;
  nameIgbo: string;
  blocks: BlockData[];
}
